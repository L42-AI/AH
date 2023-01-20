import classes.Algorithms.mutate as MutateClass

import copy

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

                M = MutateClass.Mutate(self.df, self.course_list, self.student_list, self.current_roster)
                self.step_method(M)

                # calculate the maluspoints
                self.current_roster.total_malus(self.student_list)
                self.current_malus_points = self.current_roster.malus_count

                if self.best_malus_score > self.current_malus_points:
                    self.best_roster = self.current_roster
                    self.best_malus_score = self.current_malus_points
                    self.get_name()

            self.roster_list.append(self.best_roster)
            print(self.best_roster.malus_cause)
        return self.best_roster

class HC_LectureLocate(__HillClimber):
    def step_method(self, M):
        M.swap_lecture_empty_room()

class HC_LectureSwap(__HillClimber):
    def step_method(self, M):
        M.swap_random_lessons(True)
        M.swap_random_lessons(False)

class HC_StudentSwap(__HillClimber):
    def step_method(self, M):
        M.swap_2_students()
        
    def get_name(self):
        print("students swapped random")

class HC_StudentSwapRandom(__HillClimber):
    def step_method(self, M):
        M.swap_2_students_random()

class HC_StudentSwitch(__HillClimber):
    def step_method(self, M):
        M.change_student_group()

# class HC_WorstStudentRandomGroup(__HillClimber):
#     def step_method(self, M):
#         M.swap_worst_student()