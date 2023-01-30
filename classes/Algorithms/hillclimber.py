import classes.algorithms.mutate as MutateClass
import random
import copy
import numpy as np

""" Main HillClimber Class """

class HillClimber:
    def __init__(self, schedule, course_list, student_list, MC, multiplier=0.1):
        self.schedule_list = []
        self.course_list = course_list
        self.student_list = student_list
        self.schedule = schedule
        self.MC = MC
        self.multiplier = multiplier

    """ Inheritable methods """

    def step_method(self, M):
        '''calls on a hillclimber specific step method'''
        pass

    def get_name(self):
        '''helps with keeping track of what hillclimber does what'''
        pass

    def make_mutate(self, schedule):
        '''Calls a mutate class. Can be easily changed when using different hillclimbers
           to call on a different mutate with different criterea'''
        M = MutateClass.Mutate(self.course_list, self.student_list, schedule)
        return M

    def get_score(self):
        '''Returns the total score of the current schedule'''
        return self.MC.compute_total_malus(self.schedule)['Total']


    """ Main Method """

    def climb(self, T):
        '''performs the climbing of a hillclimber. This method is inherited by every
           kind of hillclimber because it calls on make_mutate and step_methdod, allowing
           it to be easily changed when we want different kinds of hillclimbers. The
           self.double is not used by the program but serves as an analitical tool
           to inspect where double hours originate from'''

        self.double = {'l': set(), 't': set(), 'p': set()}

        # Compute malus with MalusCalculator
        self.malus = self.MC.compute_total_malus(self.schedule)

        # set the iteration to 0
        iteration = 0

        # list with the malus points and the iteration
        list_iterations = []
        list_malus = []

        # Append the input roster
        self.schedule_list.append(self.schedule)
        double_hc = {'l': {'v': 0, 'student': []}, 't': {'v': 0, 'student': []}, 'p': {'v': 0, 'student': []}}

        # let the hillclimber take some steps
        # you can change if you want multiplier for now I want always 50
        for _ in range(int(self.malus['Total'] * self.multiplier)):
        # for i in range(50):
            # self.malus = self.MC.compute_total_malus(self.schedule)
            iteration += 1

            # Make copy of schedule, complex because of dictionary
            copied_schedule = copy.deepcopy(self.schedule)

            # {k: {k2: {k3: [student for student in v3] for k3, v3 in v2.items()} for k2, v2 in v.items()} for k, v in self.schedule.items()}
            # Create the mutate class
            M = self.make_mutate(copied_schedule)

            # Take a step
            self.step_method(M)

            # Create a new variable to store the new schedule
            new_schedule = M.schedule

            # Calculate the malus points for the new schedule
            new_malus = self.MC.compute_total_malus(new_schedule)

            # if new_malus['Total'] < self.malus['Total']:
            list_iterations.append(iteration)
            list_malus.append(new_malus['Total'])

            # let the hillclimber make 3 changes before a new score is calculated
            self.__accept_schedule(new_malus, new_schedule, T, double_hc, M, _)

        # Return new roster
        return self.schedule, self.malus, list_iterations, list_malus

    def __accept_schedule(self, new_malus, new_schedule, T, double_hc, M, _):
        '''Takes in the new malus (dict) and schedule (dict) and compares it to the current version
           If it is better, it will update the self.schedule and malus'''


        # only accept annealing if the rise in malus is not too large
        difference = self.malus['Total'] - new_malus['Total']

        # if difference = 0 it will overflow
        if difference < 0.01:
            prob = 1
        elif T != 0:
            prob = 1
        else:
            prob = 1

        # Compare with prior malus points
        if new_malus['Total'] <= self.malus['Total']:
            # print(self.get_name(), self.malus['Total'], new_malus['Total'])
            self.schedule = new_schedule
            self.malus = new_malus
            double_hc['l']['v'] += M.double['l']['v']
            double_hc['t']['v'] += M.double['t']['v']
            double_hc['p']['v'] += M.double['p']['v']
            double_hc['l']['student'].append(M.double['l']['student'])
            double_hc['t']['student'].append(M.double['t']['student'])
            double_hc['p']['student'].append(M.double['p']['student'])
            
            for key in double_hc:

                if double_hc[key]['student']:
                    for student in double_hc[key]['student']:
                        if student:
                            for id in student:
                                if id not in self.double[key]:
                                    self.double[key].add(id)
        elif prob < T and _ < 1 and difference > - (100 - (1-T*200)):
            print(f'worsening of {-difference} got accepted at T: {T}')
            self.schedule = new_schedule
            self.malus = new_malus

""" Inherited HillClimber Classes """

class HC_TimeSlotSwapRandom(HillClimber):
    '''swaps a random class with another random class, calls on its own
       mutate method to swap 2 random lessons, either lectures, tutorials or practicals'''
    def step_method(self, M):

        # Take a random state to pass to function
        state = random.choice((True, False))
        M.swap_random_lessons(state)

    def get_name(self):
        return "TimeSlotSwapRandom"

class HC_TimeSlotSwapCapacity(HC_TimeSlotSwapRandom):
    '''swaps the class that has the most capacity malus points with a random class'''
    def make_mutate(self, schedule):
        M = MutateClass.Mutate_Course_Swap_Capacity(self.course_list, self.student_list, schedule)
        return M

    def get_name(self):
        return "TimeSlotSwapCapacity"

class HC_SwapBadTimeslots_GapHour(HillClimber):
    '''This class takes a random student and finds the day with the most gap hours.
       When found, it will swap one tut or pract with a student from a different group
       that has the most malus points from that group'''

    def step_method(self, M):
        M.swap_bad_timeslots()

    def get_name(self):
        return 'SwapBadTimeslots_GapHour'

class HC_SwapBadTimeslots_DoubleClasses(HillClimber):
    '''This class takes a random student and finds the day with the most double classes.
       When found, it will swap one tut or pract with a student from a different group
       that has the most malus points from that group'''

    def make_mutate(self, schedule):
        M = MutateClass.Mutate_double_classes(self.course_list, self.student_list, schedule)
        return M

    def step_method(self, M):
        M.swap_bad_timeslots()

    def get_name(self):
        return 'SwapBadTimeslots_DoubleClasses'