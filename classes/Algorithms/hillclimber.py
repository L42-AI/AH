import classes.Algorithms.mutate as MutateClass
import math
import copy
import random

class __HillClimber():
    def __init__(self, Roster, df, course_list, student_list):
        self.roster_list = []
        self.course_list = course_list
        self.student_list = student_list
        self.df = df
        self.Roster = Roster

    def step_method(self, M):
        pass

    def get_name(self):
        pass

    def climb(self):

        # set best roster and malus score
        self.best_roster = self.Roster
        self.best_malus_score = self.best_roster.malus_count

        # append the original roster
        self.roster_list.append(self.best_roster)

        for _ in range(1):
            for _ in range(50):

                # make a deep copy, initiate the swapper with the right roster and change that roster
                self.current_roster = copy.deepcopy(self.best_roster)

                M = self.make_mutate()
                
                self.step_method(M)
                self.current_roster.init_student_timeslots(self.student_list)
                
                # calculate the maluspoints
                self.current_roster.student_list = M.student_list
                self.current_roster.init_student_timeslots(self.current_roster.student_list)
                self.current_roster.total_malus(self.student_list)
                self.current_malus_points = self.current_roster.malus_count

                if self.best_malus_score > self.current_malus_points:
                    self.best_roster = self.current_roster
                    self.best_malus_score = self.current_malus_points
                    self.get_name()

            print(self.best_roster.malus_cause)

        return self.best_roster

    def replace_roster(self, T=None):
        self.current_best_roster = min(self.rosters, key=lambda x: x.malus_count)

        if self.best_malus_score > self.current_best_roster.malus_count:
            self.best_roster = self.current_best_roster

    def make_mutate(self):
        M = MutateClass.Mutate(self.df, self.course_list, self.student_list, self.current_roster)
        return M
            
class HC_LectureLocate(__HillClimber):
    def step_method(self, M):
        M.swap_lecture_empty_room()

    def get_name(self):
        print("Lesson Swapped Empty Room")

class HC_LectureSwap(__HillClimber):
    def step_method(self, M):
        M.swap_random_lessons(True)
        M.swap_random_lessons(False)

    def get_name(self):
        print("Lesson Swapped")

class HC_StudentSwap(__HillClimber):
    def step_method(self, M):
        M.swap_2_students()

    def get_name(self):
        print("Students Swapped")

class HC_StudentSwapRandom(__HillClimber):
    def step_method(self, M):
        M.swap_2_students_random()

    def get_name(self):
        print("Student Swapped Random")

class HC_StudentSwitch(__HillClimber):
    def step_method(self, M):
        M.change_student_group()

class HC_SwapBadTimeslots_GapHour(__HillClimber):
    '''This class takes a random student and finds the day with the most gap hours.
       When found, it will swap one tut or pract with a student from a different group
       that has the most malus points from that group'''
    def step_method(self, M):
        M.swap_bad_timeslots()

class HC_SwapBadTimeslots_DoubleClasses(__HillClimber):
    '''This class takes a random student and finds the day with the most double classes.
       When found, it will swap one tut or pract with a student from a different group
       that has the most malus points from that group'''
    def make_mutate(self):
        M = MutateClass.Mutate_double_classes(self.df, self.course_list, self.student_list, self.current_roster)
        return M
    def step_method(self, M):
        M.swap_bad_timeslots()








class Simulated_Annealing(__HillClimber):

    def replace_roster(self, T):

            if self.best_malus_score > self.current_malus_points:
                self.best_roster = self.current_roster
                self.best_malus_score = self.current_malus_points
            
            else: 
                p = math.exp(- (self.best_malus_score - self.current_malus_points) / T)
                randint = random.random()
                if randint <= p:
                    self.best_roster = self.current_roster
                    self.best_malus_score = self.current_malus_points

class SA_LectureLocate(Simulated_Annealing):
    def step_method(self, M):
        M.swap_lecture_empty_room()

class SA_LectureSwap(Simulated_Annealing):
    def step_method(self, M):
        M.swap_2_lectures()

class SA_StudentSwap(Simulated_Annealing):
    def step_method(self, M):
        M.swap_worst_student()

class SA_StudentSwapRandom(Simulated_Annealing):
    def step_method(self, M):
        M.swap_2_students_random()
    def get_name(self):
        print("StS")

class SA_StudentSwitch(Simulated_Annealing):
    def step_method(self, M):
        M.change_student_group()