import classes.Algorithms.hillclimber as HillCLimberClass
from multiprocessing import Pool
import random as random

import csv
import copy
import matplotlib.pyplot as plt

class HCMultiprocessor():
    def __init__(self, Roster, course_list, student_list):
        self.Roster = Roster
        self.course_list = course_list
        self.student_list = student_list

    def run_hillclimbers(self, visualize=False):

        iterations_list = []
        function1 = []
        function2 = []
        function3 = []
        function4 = []

        iter_counter = 0
        self.fail_counter = 0
        print(f'\nInitialization')
        print(self.Roster.malus_cause)
        # while self.Roster.malus_cause['Dubble Classes'] != 0 or self.Roster.malus_cause['Capacity'] != 0:
        while iter_counter < 300 and self.fail_counter < 10:

            # Increase iter counter
            iter_counter += 1

            # Make four deepcopys for each function to use
            self.rosters = [copy.deepcopy(self.Roster) for _ in range(4)]

            # Fill the pool with all functions and their rosters
            with Pool(4) as p:
                self.output_rosters = p.map(self.run_HC, [(0, self.Roster), (1, self.Roster), (2, self.Roster), (3, self.Roster)])
            # # Save data for ML
            # for i in range(4):
            #     info = (iter_counter, {f'HC{i + 1}': self.Roster.malus_count - self.output_rosters[i].malus_count})
            #     self.save_results(info)

            # Save data for plotting
            iterations_list.append(iter_counter)
            function1.append(self.Roster.malus_count - self.output_rosters[0].malus_count)
            function2.append(self.Roster.malus_count - self.output_rosters[1].malus_count)
            function3.append(self.Roster.malus_count - self.output_rosters[2].malus_count)
            function4.append(self.Roster.malus_count - self.output_rosters[3].malus_count)

            
            # find the lowest malus of the output rosters
            min_malus = min([i.malus_count for i in self.output_rosters])

            # Use the lowest malus to find the index of the best roster
            self.best_index = [i.malus_count for i in self.output_rosters].index(min_malus)

            # Compute difference between new roster and current roster
            difference = self.Roster.malus_count - self.output_rosters[self.best_index].malus_count

            # replace the roster if it is better
            self._replace_roster(difference, iter_counter)

        if visualize:
            self.plot_results(iterations_list, function1, function2, function3, function4)

    def run_HC(self, hc_tuple, t=None):

        number, roster = hc_tuple
        if number == 0:
            # print('looking to swap classes...')
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(roster, self.course_list, self.student_list)
            roster = HC1.climb(T=t)
            # print(f'HC1: {roster.malus_count}')
            return roster

        elif number == 1:
            # print('looking to swap students randomly...')
            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(roster, self.course_list, self.student_list)
            roster = HC2.climb(T=t)
            # print(f'HC2: {roster.malus_count}')
            return roster

        elif number == 2:
            # print('looking to swap students on gap hour malus...')
            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(roster, self.course_list, self.student_list)
            roster = HC3.climb(T=t)
            # print(f'HC3: {roster.malus_count}')
            return roster

        elif number == 3:
            # print('looking to swap students on double classes malus...')
            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(roster, self.course_list, self.student_list)
            roster = HC4.climb(T=t)
            # print(f'HC4: {roster.malus_count}')
            return roster

    def save_results(self, info):
        iter, dict_pair = info
        with open('data/HCresults.csv', mode='a') as f:

            string = f'{iter},{list(dict_pair.keys())[0]},{list(dict_pair.values())[0]}'
            f.write(f'\n{string}')

    def plot_results(self, iterations_list, function1, function2, function3, function4):
        plt.plot(iterations_list, function1, '-r', label = 'SwapClasses')
        plt.plot(iterations_list, function2, '-g', label = 'StudentSwapRandom')
        plt.plot(iterations_list, function3, '-m', label = 'StudentSwapGapHours')
        plt.plot(iterations_list, function4, '-b', label = 'StudentSwapDoubleHours')
        plt.legend()
        plt.show()

    def _replace_roster(self, difference, iter_count):

        # If difference is positive
        if difference > 0:

            # Set the new roster to self.Roster
            self.Roster = self.output_rosters[self.best_index]
            self.fail_counter = 0

            print(f'\n========================= Generation: {iter_count} =========================\n')
            print(f'Most effective function: HC{self.best_index + 1}')
            print(f'Malus improvement: {difference}')
            print(self.Roster.malus_cause)

        else:
            self.fail_counter += 1

            # print output
            print(f'\n========================= Generation: {iter_count} =========================\n')
            print('FAIL')
            print(self.Roster.malus_cause)

# class HCMultiprocessor_SimAnnealing(HCMultiprocessor):
    
#     def _replace_roster(self, difference, iter_count):
#         # set the temperature
#         T = (150/(200 + iter_count*2))

#         # If difference is positive
#         if difference > 0:

#             # Set the new roster to self.Roster
#             self.Roster = self.output_rosters[self.best_index]
#             self.fail_counter = 0

#             print(f'\n========================= Generation: {iter_count} =========================\n')
#             print(f'Most effective function: HC{self.best_index + 1}')
#             print(f'Malus improvement: {difference}')
#             print(self.Roster.malus_cause)

#         elif difference < 0:
#             prob = random.random()
#             if prob < T:
#                 self.Roster = random.choice(self.output_rosters)
#                 self.fail_counter = 0

#                 # print output
#                 print(f'\n========================= Generation: {iter_count} =========================\n')
#                 print(f'FAIL GOT ACCEPTED WITH T AT: {T}')
#                 print(self.Roster.malus_cause)

#             else:
#                 self.fail_counter += 1

#                 # print output
#                 print(f'\n========================= Generation: {iter_count} =========================\n')
#                 print('FAIL')
#                 print(self.Roster.malus_cause)