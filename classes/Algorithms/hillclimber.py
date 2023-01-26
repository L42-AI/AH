import classes.Algorithms.mutate as MutateClass
import random
import copy

""" Main HillClimber Class """

class HillClimber:
    def __init__(self, schedule, course_list, student_list, MC):
        self.roster_list = []
        self.course_list = course_list
        self.student_list = student_list
        self.schedule = schedule
        self.MC = MC

    """ Inheritable methods """

    def step_method(self, M):
        pass

    def get_name(self):
        pass

    # Aangezien dit nooit wordt gebruikt, verwijderen en pass neerzetten?
    def make_mutate(self, schedule):
        M = MutateClass.Mutate(self.course_list, self.student_list, schedule)
        return M


    # Aangezien dit nooit wordt gebruikt, verwijderen en pass neerzetten?
    def replace_roster(self, T=None):
        self.current_best_roster = min(self.rosters, key=lambda x: x.malus_count)

        if self.best_malus > self.current_best_roster.malus_count:
            self.best_schedule = self.current_best_roster

    """ Main Method """

    def climb(self, T=None):

        # Set input roster as best roster and best malus count
        self.best_schedule = self.schedule

        # Compute malus with MalusCalculator
        self.best_malus = self.MC.compute_total_malus(self.schedule)

        # Append the input roster
        self.roster_list.append(self.best_schedule)

        # Take 50 steps:
        for _ in range(50):

            # Set current roster
            current_schedule = self.best_schedule

            # Make copy of schedule, complex because of dictionary
            copied_schedule = {k: {k2: {k3: v3 for k3, v3 in v2.items()} for k2, v2 in v.items()} for k, v in current_schedule.items()}

            # Create the mutate class
            M = self.make_mutate(copied_schedule)

            # Take a step
            self.step_method(M)

            # Create a new variable to store the new schedule
            new_schedule = M.schedule

            # Calculate the malus points for the new schedule
            new_malus = self.MC.compute_total_malus(new_schedule)

            # Compare with prior malus points
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            self.__accept_schedule(new_malus, new_schedule, T)
=======
=======
>>>>>>> 0c9155501a485d7eb3bd063eb4e2de2c6a0c9f4b
=======
>>>>>>> 97a96e265fc443e44531d8ca29b91a54d5b658eb
            if new_malus['Total'] < self.best_malus['Total']:

                self.best_schedule = new_schedule
                self.best_malus = new_malus
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 2e7f291ccf4c5f703c6e7a9e4da36d1e21d18458
=======
>>>>>>> 0c9155501a485d7eb3bd063eb4e2de2c6a0c9f4b
=======
>>>>>>> 97a96e265fc443e44531d8ca29b91a54d5b658eb

                # Print method name
                # print(self.get_name())

        # Return new roster
        return self.best_schedule, self.best_malus
<<<<<<< HEAD
<<<<<<< HEAD

    def __accept_schedule(self, new_malus, new_schedule, T):
        prob = random.random()
        if prob < T or new_malus['Total'] < self.best_malus_count['Total']:
            self.best_roster.schedule = new_schedule
            self.best_malus_count = new_malus
=======
>>>>>>> 0c9155501a485d7eb3bd063eb4e2de2c6a0c9f4b
=======
>>>>>>> 97a96e265fc443e44531d8ca29b91a54d5b658eb

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

class SA_TimeSlotSwapRandom(HC_TimeSlotSwapRandom):
    def __accept_schedule(self, new_malus, new_schedule, T):
        prob = random.random()
        if prob < T or new_malus['Total'] < self.best_malus_count['Total']:
            self.best_roster.schedule = new_schedule
            self.best_malus_count = new_malus

