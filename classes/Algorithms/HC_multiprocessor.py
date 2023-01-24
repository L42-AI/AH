import classes.Algorithms.hillclimber as HillCLimberClass
from multiprocessing import Pool
import random as random

import time
import json
import copy
import matplotlib.pyplot as plt

class HCMultiprocessor():
    def __init__(self, Roster, course_list, student_list):
        self.Roster = Roster
        self.course_list = course_list
        self.student_list = student_list

    def run_hillclimbers(self):

        # Set lists
        self.iterations_list = []
        self.info = {}

        # Set counters
        self.iter_counter = 0
        self.fail_counter = 0

        self.duration = 0

        # Print intitial
        print(f'\nInitialization')
        print(self.Roster.malus_cause, self.Roster.malus_count)

        # while self.Roster.malus_cause['Dubble Classes'] != 0 or self.Roster.malus_cause['Capacity'] != 0:
        while self.iter_counter != 100:

            start_time = time.time()

            # Make four deepcopys for each function to use
            self.rosters = [copy.deepcopy(self.Roster) for _ in range(4)]

            # Fill the pool with all functions and their rosters
            with Pool(4) as p:
                self.output_rosters = p.map(self.run_HC, [(0, self.rosters[0]), (1, self.rosters[1]), (2, self.rosters[2]), (3, self.rosters[3])])

            print(self.output_rosters)

            # Save data for plotting
            self.iterations_list.append(self.iter_counter)

            # find the lowest malus of the output rosters
            min_malus = min([i.malus_count for i in self.output_rosters])

            # Use the lowest malus to find the index of the best roster
            self.best_index = [i.malus_count for i in self.output_rosters].index(min_malus)

            # Compute difference between new roster and current roster
            difference = self.Roster.malus_count - self.output_rosters[self.best_index].malus_count

            finish_time = time.time()

            self.iter_duration = finish_time - start_time
            self.duration += self.iter_duration

            # replace the roster if it is better
            self.__replace_roster(difference)

            # Increase iter counter
            self.iter_counter += 1

    def run_HC(self, hc_tuple):
        number, roster = hc_tuple
        if number == 0:
            # print('looking to swap classes...')
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(roster, self.course_list, self.student_list)
            roster = HC1.climb()
            # print(f'HC1: {roster.malus_count}')
            return roster

        elif number == 1:
            # print('looking to swap students randomly...')
            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(roster, self.course_list, self.student_list)
            roster = HC2.climb()
            # print(f'HC2: {roster.malus_count}')
            return roster

        elif number == 2:
            # print('looking to swap students on gap hour malus...')
            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(roster, self.course_list, self.student_list)
            roster = HC3.climb()
            # print(f'HC3: {roster.malus_count}')
            return roster

        elif number == 3:
            # print('looking to swap students on double classes malus...')
            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(roster, self.course_list, self.student_list)
            roster = HC4.climb()
            # print(f'HC4: {roster.malus_count}')
            return roster

    def save_results(self):
        if self.iter_counter not in self.info:
            self.info[self.iter_counter] = {}

        self.info[self.iter_counter]['Malus'] = self.Roster.malus_count

        for i in self.output_rosters:
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

    def __replace_roster(self, difference):

        # If difference is positive
        if difference > 0:

            # Set the new roster to self.Roster
            self.Roster = self.output_rosters[self.best_index]
            self.fail_counter = 0

            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print(f'Most effective function: HC{self.best_index + 1}')
            print(f'Malus improvement: {difference}')
            print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.Roster.malus_cause, self.Roster.malus_count)

        else:
            self.fail_counter += 1

            # print output
            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print('FAIL')
            print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.Roster.malus_cause, self.Roster.malus_count)

class HCMultiprocessor_SimAnnealing(HCMultiprocessor):

    def __replace_roster(self, difference):
        # set the temperature
        T = (150/(200 + self.iter_counter*2))

        # If difference is positive
        if difference > 0:

            # Set the new roster to self.Roster
            self.Roster = self.output_rosters[self.best_index]
            self.fail_counter = 0

            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print(f'Temperature at generation: {T}')
            print(f'Most effective function: SA{self.best_index + 1}')
            print(f'Malus improvement: {difference}')
            print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.Roster.malus_cause, self.Roster.malus_count)

        elif difference < 0:
            prob = random.random()
            if prob < T:
                self.Roster = random.choice(self.output_rosters)
                self.fail_counter = 0

                # print output
                print(f'\n========================= Generation: {self.iter_counter} =========================\n')
                print(f'FAIL GOT ACCEPTED WITH TEMPERATURE AT: {T}')
                print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
                print(f'Duration since init: {round(self.duration, 2)} S.')
                print(self.Roster.malus_cause, self.Roster.malus_count)

            else:
                self.fail_counter += 1

                # print output
                print(f'\n========================= Generation: {self.iter_counter} =========================\n')
                print('FAIL')
                print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
                print(f'Duration since init: {round(self.duration, 2)} S.')
                print(self.Roster.malus_cause, self.Roster.malus_count)