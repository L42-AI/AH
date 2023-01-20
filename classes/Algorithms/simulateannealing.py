import classes.Algorithms.mutate as MutateClass

import copy
import random
import math
class __SimulatedAnnealing():
    def __init__(self):



    def simulated_annealing(initial_schedule, temperature_function, cooling_rate):
        schedule = initial_schedule
        current_cost = schedule_cost(schedule)
        for temperature in temperature_function:
            next_schedule = schedule_neighbor(schedule)
            next_cost = schedule_cost(next_schedule)
            delta_cost = next_cost - current_cost
            if delta_cost > 0:
                schedule = next_schedule
                current_cost = next_cost
            else:
                probability = math.exp(-delta_cost / temperature)
                if probability > random.random():
                    schedule = next_schedule
                    current_cost = next_cost
            temperature *= cooling_rate
        return schedule

    def step_method(self, M):
        pass

    def anneale(self):
        self.best_roster = self.Roster
        self.best_malus_score = self.best_roster.malus_count
        temperature = self.temperature_start
        for _ in range(50):

            # make a deep copy, initiate the swapper with the right roster and change that roster
            self.current_roster = copy.deepcopy(self.best_roster)

            M = MutateClass.Mutate(self.df, self.course_list, self.student_list, self.current_roster)
            self.step_method(M)

        Doe een kleine random aanpassing
        Als random( ) > kans(oud, nieuw, temperatuur):
        Maak de aanpassing ongedaan
        Verlaag temperatuur
        Herhaal:
        Kies een random start state
        Kies start temperatuur
        Herhaal N iteraties:
        Doe een kleine random aanpassing
        Als random( ) > kans(oud, nieuw, temperatuur):
        Maak de aanpassing ongedaan
        Verlaag temperatuur