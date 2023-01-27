import classes.algorithms.hillclimber as HillCLimberClass
from multiprocessing import Pool
import random as random
import pandas as pd
import time
import json
import copy
import matplotlib.pyplot as plt

class Multiprocessor():
    def __init__(self, Roster, course_list, student_list, MC, annealing=False):
        self.Roster = Roster
        self.course_list = course_list
        self.student_list = student_list
        self.ITERS = 1000
        self.ANNEALING = annealing

        self.MC = MC

    def core_assignment(self, malus) -> list:

        core_assignment_list = []

        student_malus_proportion = (malus['Double Classes'] + malus['Classes Gap'] + malus['Triple Gap']) / malus['Total']

        schedule_malus_proportion = (malus['Night'] + malus['Capacity']) / malus['Total']

        while len(core_assignment_list) < 4:
            prob = random.random()

            if prob <= schedule_malus_proportion:
                method_used = random.randint(0,1)
                core_assignment_list.append(method_used)

            elif prob <= student_malus_proportion:
                method_used = random.randint(2,3)
                core_assignment_list.append(method_used)

        return core_assignment_list

    def run(self):

        # Set lists
        self.malus_points_total = []
        self.malus_swap_course_random = []
        self.malus_swap_course_capacity = []
        self.malus_swap_student_gaphour = []
        self.malus_swap_student_doublehour = []

        self.info = {}

        # Set counters
        self.iter_counter = 0
        self.fail_counter = 0

        # Set Initial variable
        self.duration = 0

        self.schedule = self.Roster.schedule

        self.malus = self.MC.compute_total_malus(self.schedule)

        core_assignment_list = [0,0,1,1]

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        # while self.Roster.malus_cause['Dubble Classes'] != 0 or self.Roster.malus_cause['Capacity'] != 0:
        while self.fail_counter <= 30:

            start_time = time.time()

            if self.ANNEALING:
                t = 0.25 - self.iter_counter / self.ITERS * 4
            else:
                t = 0

            start_time = time.time()

            # Fill the pool with all functions and their rosters
            with Pool(4) as p:
                self.output_schedules = p.map(self.run_HC, [(core_assignment_list[0], self.schedule, t, self.malus['Total']),
                                                            (core_assignment_list[1], self.schedule, t, self.malus['Total']),
                                                            (core_assignment_list[2], self.schedule, t, self.malus['Total']),
                                                            (core_assignment_list[3], self.schedule, t, self.malus['Total'])])

            if self.malus['Capacity'] <= 15:
                core_assignment_list = [0,1,2,3]

            # Save data for plotting
            self.iterations_list.append(self.iter_counter)

            # find the lowest malus of the output rosters
            min_malus = min([i[1]['Total'] for i in self.output_schedules])

            # Use the lowest malus to find the index of the best roster
            self.best_index = [i[1]['Total'] for i in self.output_schedules].index(min_malus)

            total_malus = self.malus['Total']
            best_total_malus = self.output_schedules[self.best_index][1]['Total']

            # Compute difference between new roster and current roster
            difference = total_malus - best_total_malus

            # Set finish time
            finish_time = time.time()

            # Save iterations, total maluspoints and each of the 4 algorithms the amount of points they drop in malus
            # in order to plot later
            self.malus_points_total.append(total_malus)

            lists = [self.malus_swap_course_random, self.malus_swap_course_capacity, self.malus_swap_student_gaphour, self.malus_swap_student_doublehour]

            # append for each heuristiek the difference of points they created
            for i, malus in enumerate(self.output_schedules):

                # check if we already had this one then dont calculate difference again
                if i == self.best_index:
                    lists[i].append(difference)
                
                else:
                    lists[i].append(total_malus - malus[1]['Total'])

            self.iter_duration = finish_time - start_time
            self.duration += self.iter_duration

            # replace the roster if it is better
            self.__replace_roster(difference)

            # Increase iter counter
            self.iter_counter += 1


    def __replace_roster(self, difference):

        # If difference is positive
        if difference > 0:

            # Set the new roster to self.Roster
            self.schedule, self.malus = self.output_schedules[self.best_index]

            self.fail_counter = 0

            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print(f'Most effective function: HC{self.best_index + 1}')
            print(f'Malus improvement: {difference}')
            print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)

        else:
            self.fail_counter += 1

            # print output
            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print('FAIL')
            print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)

    """ Hill Climbers """

    def run_HC(self, hc_tuple):
        activation, schedule, T, real_score = hc_tuple
        if activation == 0:
            # print('looking to swap classes...')
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(schedule, self.course_list, self.student_list, self.MC)

            schedule, malus = HC1.climb(T)
        
            # print(f'HC1: {roster.malus_count}')
            return schedule, malus

        elif activation == 1:
            # print('looking to swap students randomly...')
            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(schedule, self.course_list, self.student_list, self.MC)

            
            schedule, malus = HC2.climb(T)
            # print(f'HC2: {roster.malus_count}')
            return schedule, malus

        elif activation == 2:
            # print('looking to swap students on gap hour malus...')
            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(schedule, self.course_list, self.student_list, self.MC)

            schedule, malus = HC3.climb(T)
            # print(f'HC3: {roster.malus_count}')
            return schedule, malus

        elif activation == 3:
            # print('looking to swap students on double classes malus...')
            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(schedule, self.course_list, self.student_list, self.MC)
            schedule, malus = HC4.climb(T)
            # print(f'HC4: {roster.malus_count}')
            return schedule, malus



    """ Save and Visualize Data """

    def save_results(self):
        if self.iter_counter not in self.info:
            self.info[self.iter_counter] = {}

        self.info[self.iter_counter]['Malus'] = self.Roster.malus_count

        for i in self.output_schedules:
            dict_key, dict_value = tuple(i[1].items())[0]
            self.info[self.iter_counter][dict_key] = dict_value

    def export_results(self, capacity, popular, popular_own_day):
        # Open a file for writing
        with open(f"data/HC_capacity:{capacity}_popular:{popular}_popular:{popular_own_day}.json", "w") as f:
            # Write the dictionary to the file
            json.dump(self.info, f)

    def plot_results(self, iterations_list, function1, function2, function3, function4):
        plt.plot(iterations_list, function1, '-r', label = 'SwapClasses')
        plt.plot(iterations_list, function2, '-g', label = 'StudentSwapRandom')
        plt.plot(iterations_list, function3, '-m', label = 'StudentSwapGapHours')
        plt.plot(iterations_list, function4, '-b', label = 'StudentSwapDoubleHours')
        plt.legend()
        plt.show()


class Multiprocessor_SimAnnealing(Multiprocessor):

    def __replace_roster(self, difference):
        # set the temperature
        T = (150/(200 + self.iter_counter*2))

        # If difference is positive
        if difference > 0:

            # Set the new roster to self.Roster
            self.schedule, self.malus = self.output_schedules[self.best_index]
            self.fail_counter = 0

            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print(f'Temperature at generation: {T}')
            print(f'Most effective function: SA{self.best_index + 1}')
            print(f'Malus improvement: {difference}')
            print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)

        elif difference < 0:
            prob = random.random()
            if prob < T:
                self.schedule, self.malus = random.choice(self.output_schedules)
                self.fail_counter = 0

                # print output
                print(f'\n========================= Generation: {self.iter_counter} =========================\n')
                print(f'FAIL GOT ACCEPTED WITH TEMPERATURE AT: {T}')
                print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
                print(f'Duration since init: {round(self.duration, 2)} S.')
                print(self.malus)

            else:
                self.fail_counter += 1

            # print output
            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print('FAIL')
            print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)