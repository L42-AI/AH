import classes.Algorithms.mutate_shallow as MutateClass
import copy
import random


""" Main HillClimber Class """

class HillClimber():
    def __init__(self, Roster, course_list, student_list):
        self.roster_list = []
        self.course_list = course_list
        self.student_list = student_list
        self.Roster = Roster

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

            # Set current roster
            current_roster = self.best_roster

            # Make a deep copy, initiate the swapper with the right roster and change that roster
            copied_schedule = copy.copy(current_roster.schedule)

            # Create the mutate class
            M = self.make_mutate(copied_schedule)

            # Take a step
            self.step_method(M)

            # Create a new variable to store the new schedule
            new_schedule = M.schedule

            # Calculate the malus points for the new schedule
            current_roster.schedule = new_schedule

            # Calculate the maluspoints
            current_roster.init_student_timeslots(current_roster.student_list)
            current_roster.total_malus(self.student_list)

            # Set malus points
            self.current_malus_points = current_roster.malus_count

            print(current_roster == self.Roster)
            print()
            # Compare with prior malus points
            if self.current_malus_points < self.best_malus_score:
                self.best_roster = current_roster
                self.best_malus_score = self.current_malus_points

                # Print method name
                print(self.get_name())

        # Print new malus
        # print(self.best_roster.malus_cause)

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

    def get_name(self):
        return 'Student Swapped'

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
        return 'Student Swapped'
