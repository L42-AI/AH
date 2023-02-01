import classes.algorithms.mutate as MutateClass
from helpers.shallow_copy import recursive_copy
import classes.representation.malus_calc as MalusCalculatorClass
from data.assign import student_list, course_list

import random
import copy
import numpy as np
import csv
import decimal

""" Main HillClimber Class """

class HillClimber:
    def __init__(self, schedule, iteration=0):
        self.schedule_list = []
        self.course_list = course_list
        self.student_list = student_list
        self.schedule = schedule
        self.iteration = iteration

        self.MC = MalusCalculatorClass.MC()

        # Compute malus with MalusCalculator
        self.malus = self.MC.compute_total_malus(self.schedule)

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

    def get_score(self):
        return self.MC.compute_total_malus(self.schedule)['Total']


    """ Main Method """

    def climb(self, hill_climber_iters=400, T=0, ANNEALING=False, fail_counter=None):
        self.double = {'l': set(), 't': set(), 'p': set()}
        self.accept_me = False
        # Compute malus with MalusCalculator
        self.malus = self.MC.compute_total_malus(self.schedule)

        # Append the input roster
        self.schedule_list.append(self.schedule)

        if type(hill_climber_iters) == float:
            multiplier = True
            self.hill_climber_iters = int(self.malus['total'] * hill_climber_iters)
        else:
            multiplier = False
            self.hill_climber_iters = hill_climber_iters

        # let the hillclimber take some steps 
        # for _ in range(int(self.malus['Total'] * self.multiplyer)):
        for _ in range(self.hill_climber_iters):

            # Make copy of schedule, complex because of dictionary
            copied_schedule = recursive_copy(self.schedule)

            # {k: {k2: {k3: [student for student in v3] for k3, v3 in v2.items()} for k2, v2 in v.items()} for k, v in self.schedule.items()}
            # Create the mutate class
            M = self.make_mutate(copied_schedule)

            # Take a step
            self.step_method(M)

            # Create a new variable to store the new schedule
            new_schedule = M.schedule

            # Calculate the malus points for the new schedule
            new_malus = self.MC.compute_total_malus(new_schedule)

            # self.save_results()

            # let the hillclimber make 3 changes before a new score is calculated
            self.__accept_schedule(new_malus, new_schedule, T=T, ANNEALING=ANNEALING, fail_counter=fail_counter)

            self.iteration += 1

            if multiplier:
                self.hill_climber_iters = int(self.malus['total'] * hill_climber_iters)

        return self.schedule, self.malus, self.iteration, self.accept_me

    def __accept_schedule(self, new_malus, new_schedule, T=0, ANNEALING=False, fail_counter=None):
        '''Takes in the new malus (dict) and schedule (dict) and compares it to the current version
           If it is better, it will update the self.schedule and malus'''

        prob = random.random()
        # only accept annealing if the rise in malus is not too large
        difference = self.malus['Total'] - new_malus['Total']

        # only accept annealing if the rise in malus is not too large
        difference = self.malus['Total'] - new_malus['Total']
        prob = random.random()

        # create an accept threshold when using simulated annealing
        if new_malus['Total'] < 120 and ANNEALING and not self.accept_me and fail_counter > 500:
            accept = decimal.Decimal(1 - np.exp(-difference/T))
        else:
            accept = 2 # 2 can never be accepted

        # Compare with prior malus points
        if new_malus['Total'] <= self.malus['Total']:
            self.schedule = new_schedule
            self.malus = new_malus

        elif prob > accept and difference < 20:
            T = 0
            # print(f'worsening of {-difference} got accepted at T: {T}')
            self.schedule = new_schedule
            self.malus = new_malus
            self.accept_me = True



    def save_results_multi(self):
        with open('data/HCResults.csv', 'a') as f:
            csv_writer = csv.DictWriter(f, fieldnames=['HC1 type','HC1 iteration','HC1 malus','HC2 type','HC2 iteration','HC2 malus','HC3 type','HC3 iteration','HC3 malus','HC4 type','HC4 iteration','HC4 malus'])
            info = {
                f'HC{self.core_assignment} type': self.get_name(),
                f'HC{self.core_assignment} iteration': self.iteration,
                f'HC{self.core_assignment} malus': self.malus['Total']
            }

            csv_writer.writerow(info)

    def save_results(self):
        with open('data/HCResults.csv', 'a') as f:
            csv_writer = csv.DictWriter(f, fieldnames=['HC type','HC iteration','HC malus'])
            info = {
                f'HC type': self.get_name(),
                f'HC iteration': self.iteration,
                f'HC malus': self.malus['Total']
            }

            csv_writer.writerow(info)

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