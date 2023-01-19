import classes.Algorithms.mutate as MutateClass

import copy

class HillClimber():
    def __init__(self, Roster, df, course_list, student_list):
        self.roster_list = []
        self.course_list = course_list
        self.student_list = student_list
        self.df = df
        self.Roster = Roster

    def set_roster(self):
        # set best roster and malus score
        self.best_roster = self.Roster
        self.best_malus_score = self.best_roster.malus_count
        # append the original roster
        self.roster_list.append(self.best_roster)

    def step_method(self, M):
        M.swap_lecture_empty_room()

    def step(self):
        # make a deep copy, initiate the swapper with the right roster and change that roster
        self.current_roster = copy.deepcopy(self.best_roster)
        M = MutateClass.Mutate(self.df, self.course_list, self.student_list, self.current_roster)
        self.step_method(M)

    def calc_malus(self):
        # calculate the maluspoints
        self.current_roster.total_malus(self.student_list)
        self.current_malus_points = self.current_roster.malus_count

    def set_better(self):
        # if the malus points are lower then the previous lowest malus points set the best to the new object
        if self.best_malus_score > self.current_malus_points:
            self.best_roster = self.current_roster
            self.best_malus_score = self.current_malus_points

    def save_better(self):
        # append the new best roster
        self.roster_list.append(self.best_roster)
        print(self.best_malus_score)

    def climb(self):

        self.set_roster()

        for _ in range(1):
            for _ in range(50):
                self.step()
                self.calc_malus()
                self.set_better()
            self.save_better()

class HC_LectureLocate(HillClimber):
    def step_method(self, M):
        M.swap_lecture_empty_room()

class HC_LectureSwap(HillClimber):
    def step_method(self, M):
        M.swap_2_lectures()

class HC_StudentSwap(HillClimber):
    def step_method(self, M):
        M.swap_2_students_random()

class HC_WorstStudentRandomGroup(HillClimber):
    def step_method(self, M):
        M.swap_worst_student()