import classes.Algorithms.mutate as MutateClass
import copy
import random

""" Main HillClimber Class """

class HillClimber():
    def __init__(self, Roster, df, course_list, student_list):
        self.roster_list = []
        self.course_list = course_list
        self.student_list = student_list
        self.df = df
        self.Roster = Roster

    """ Inheritable methods """

    def step_method(self, M):
        pass

    def get_name(self):
        pass

    def make_mutate(self):
        M = MutateClass.Mutate(self.df, self.course_list, self.student_list, self.current_roster)
        return M

    def replace_roster(self, T=None):
        self.current_best_roster = min(self.rosters, key=lambda x: x.malus_count)

        if self.best_malus_score > self.current_best_roster.malus_count:
            self.best_roster = self.current_best_roster

    """ Main Method """

    def climb(self):

        # Set input roster as best roster and best malus count
        self.best_roster = self.Roster
        self.best_malus_score = self.best_roster.malus_count

        # Append the input roster
        self.roster_list.append(self.best_roster)

        # Take 50 steps:
        for _ in range(50):

            # Make a deep copy, initiate the swapper with the right roster and change that roster
            self.current_roster = copy.deepcopy(self.best_roster)

            # Create the mutate class
            M = self.make_mutate()

            # Take a step
            self.step_method(M)

            # Set changed student list to roster student list
            self.current_roster.student_list = M.student_list

            # Calculate the maluspoints
            self.current_roster.init_student_timeslots(self.current_roster.student_list)
            self.current_roster.total_malus(self.student_list)

            # Set malus points
            self.current_malus_points = self.current_roster.malus_count

            # Compare with prior malus points
            if self.best_malus_score > self.current_malus_points:
                self.best_roster = self.current_roster
                self.best_malus_score = self.current_malus_points

                # Print method name
                self.get_name()

        # Print new malus
        print(self.best_roster.malus_cause)

        # Return new roster
        return self.best_roster

""" Inherited HillClimber Classes """

""" Step method bestaat niet meer, zit in lecture swap? """
# class HC_LectureLocate(HillClimber):

#     def step_method(self, M):
#         M.swap_lecture_empty_room()

class HC_LectureSwap(HillClimber):

    def step_method(self, M):

        # Take a random state to pass to function
        state = random.choice((True, False))
        M.swap_random_lessons(state)

    def get_name(self):
        return "Lesson Swapped"

class HC_StudentSwap(HillClimber):

    def step_method(self, M):
        M.swap_2_students()

    def get_name(self):
        return "Students Swapped"

class HC_SwapBadTimeslots_GapHour(HillClimber):
    '''This class takes a random student and finds the day with the most gap hours.
       When found, it will swap one tut or pract with a student from a different group
       that has the most malus points from that group'''

    def step_method(self, M):
        M.swap_bad_timeslots()

class HC_SwapBadTimeslots_DoubleClasses(HillClimber):
    '''This class takes a random student and finds the day with the most double classes.
       When found, it will swap one tut or pract with a student from a different group
       that has the most malus points from that group'''

    def make_mutate(self):
        M = MutateClass.Mutate_double_classes(self.df, self.course_list, self.student_list, self.current_roster)
        return M

    def step_method(self, M):
        M.swap_bad_timeslots()
