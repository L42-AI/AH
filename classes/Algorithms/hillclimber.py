import classes.algorithms.mutate as MutateClass
import random
import copy

""" Main HillClimber Class """

class HillClimber:
    def __init__(self, schedule, course_list, student_list, MC):
        self.schedule_list = []
        self.course_list = course_list
        self.student_list = student_list
        self.schedule = schedule
        self.MC = MC

        self.multiplyer = 1

    """ Inheritable methods """

    def step_method(self, M):
        pass

    def get_name(self):
        pass

    def make_mutate(self, schedule):
        M = MutateClass.Mutate(self.course_list, self.student_list, schedule)
        return M

    def replace_roster(self, T=None):
        self.current_best_roster = min(self.rosters, key=lambda x: x.malus_count)

        if self.best_malus > self.current_best_roster.malus_count:
            self.best_schedule = self.current_best_roster

    """ Main Method """

    def climb(self, T):

        # Compute malus with MalusCalculator
        self.malus = self.MC.compute_total_malus(self.schedule)

        # Append the input roster
        self.schedule_list.append(self.schedule)

        # Take 50 steps:
        # while (self.malus['Total'] - start_malus['Total']) / start_malus['Total'] < 0.2:
        for _ in range(int(self.malus['Total'] * self.multiplyer)):

            # Make copy of schedule, complex because of dictionary
            copied_schedule = {k: {k2: {k3: v3 for k3, v3 in v2.items()} for k2, v2 in v.items()} for k, v in self.schedule.items()}

            # Create the mutate class
            M = self.make_mutate(copied_schedule)

            print(self.malus)

            # Take a step
            self.step_method(M)

            # Create a new variable to store the new schedule
            new_schedule = M.schedule

            # Calculate the malus points for the new schedule
            new_malus = self.MC.compute_total_malus(new_schedule)

            print(new_malus)

            self.__accept_schedule(new_malus, new_schedule, T)

        # Return new roster
        return self.schedule, self.malus

    def __accept_schedule(self, new_malus, new_schedule, T):

        prob = random.random()

        # only accept annealing if the rise in malus is not too large
        difference = self.malus['Total'] - new_malus['Total']
        five_percent = self.malus['Total'] * 0.05

        # Compare with prior malus points
        if new_malus['Total'] < self.malus['Total']:
            # print(self.get_name(), self.malus['Total'], new_malus['Total'])
            self.schedule = new_schedule
            self.malus = new_malus

        elif prob < T and difference < five_percent:
            print(f'worsening of {difference} got accepted at T: {T}')
            self.schedule = new_schedule
            self.malus = new_malus

""" Inherited HillClimber Classes """

class HC_TimeSlotSwapRandom(HillClimber):
    '''swaps a random class with another random class'''
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