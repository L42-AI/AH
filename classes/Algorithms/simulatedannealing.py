import classes.Algorithms.hillclimber as HillClimberClass
import random
import math


class Simulated_Annealing(HillClimberClass.HillClimber):

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

""" Step method bestaat niet meer, zit in lecture swap? """
# class SA_LectureLocate(Simulated_Annealing):
#     def step_method(self, M):
#         M.swap_lecture_empty_room()

class SA_LectureSwap(Simulated_Annealing):
    def step_method(self, M):

        # Take a random state to pass to function
        state = random.choice((True, False))
        M.swap_random_lessons(state)

    def get_name(self):
        return "Lesson Swapped"

class SA_StudentSwap(Simulated_Annealing):
    def step_method(self, M):
        M.swap_2_students()

    def get_name(self):
        return "Students Swapped"

""" Missen nog beide swap bad timeslots """