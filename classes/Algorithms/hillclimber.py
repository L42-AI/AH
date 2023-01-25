import classes.Algorithms.mutate as MutateClass
import random
import copy

""" Main HillClimber Class """

class HillClimber:
    def __init__(self, Roster, course_list, student_list, MC):
        self.roster_list = []
        self.course_list = course_list
        self.student_list = student_list
        self.Roster = Roster
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

        if self.best_malus_count > self.current_best_roster.malus_count:
            self.best_roster = self.current_best_roster

    """ Main Method """

    def climb(self):

        # Set input roster as best roster and best malus count
        self.best_roster = self.Roster

        # Compute malus with MalusCalculator
        self.best_malus_count = self.MC.compute_total_malus(self.best_roster.schedule)

        # Append the input roster
        self.roster_list.append(self.best_roster)

        # Take 30 steps:
        for _ in range(1):

            # Set current roster
            current_roster = self.best_roster

            # Make copy of schedule, complex because of dictionary
            copied_schedule = {k: {k2: {k3: v3 for k3, v3 in v2.items()} for k2, v2 in v.items()} for k, v in current_roster.schedule.items()}

            # Create the mutate class
            M = self.make_mutate(copied_schedule)

            # Take a step
            self.step_method(M)

            # Create a new variable to store the new schedule
            new_schedule = M.schedule

            # Calculate the malus points for the new schedule
            new_malus = self.MC.compute_total_malus(new_schedule)

            # Compare with prior malus points
            if new_malus['Total'] < self.best_malus_count['Total']:

                self.best_roster.schedule = new_schedule
                self.best_malus_count = new_malus

                # Print method name
                # print(self.get_name())

        # Return new roster
        return self.best_roster, self.best_malus_count

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
