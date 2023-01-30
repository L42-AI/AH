import classes.algorithms.hillclimber as HillCLimberClass
from multiprocessing import Pool
import random
import classes.GUI.selector_GUI as SelectorApp

import csv
import time
import json
import copy
import matplotlib.pyplot as plt


class Multiprocessor():
    def __init__(self, Roster, course_list, student_list, MC, annealing, core_arrangement):
        self.Roster = Roster
        self.course_list = course_list
        self.student_list = student_list
        self.ITERS = 1
        self.ANNEALING = annealing
        self.core_arrangement = core_arrangement

        self.MC = MC

    def core_assignment(self, malus) -> list:

        core_assignment_list = []

        student_malus_proportion = (malus['Double Classes'] + malus['Classes Gap'] + malus['Triple Gap']) / malus['Total']

        schedule_malus_proportion = 1 - (malus['Night'] + malus['Capacity']) / malus['Total']

        while len(core_assignment_list) < 4:
            prob = random.random()

            if prob <= schedule_malus_proportion:
                method_used = random.randint(0,1)
                core_assignment_list.append(method_used)

            elif prob <= student_malus_proportion:
                method_used = random.randint(2,3)
                core_assignment_list.append(method_used)

        return core_assignment_list

    def __init_temp(self) -> float:
        if self.ANNEALING:
            return .8
        else:
            return float(0)

    def __set_temp(self, T) -> float:
        if self.ANNEALING:
            if T > .5:
                return self.__get_temperature(T)
            elif T <= .5:
                T = self.__get_temperature(T, alpha=0.65)

            if T < 0.01:
                return 0.05
        else:
            return 0

    def run_combination(self, mode):
        # Set counters
        self.fail_counter = 0
        self.multiprocessor_counter = 0
        self.hillclimber_counter = 0
        self.duration = 0

        self.schedule = self.Roster.schedule
        self.malus = self.MC.compute_total_malus(self.schedule)

        T = self.__init_temp()

        # Initialize all hillclimbers
        HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter)
        HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter)
        HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter)
        HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter)


        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        # Run the optimizing loop
        while self.malus['Total'] > 100:

            start_time = time.time()

            while self.malus['Total'] > 200:

                self.schedule, self.malus, self.hillclimber_counter = HC1.climb(T)

                HC1.schedule = self.schedule
                HC1.iteration = self.hillclimber_counter

                print(self.malus)

            HC2.schedule = self.schedule
            HC2.iteration = self.hillclimber_counter

            HC3.schedule = self.schedule
            HC3.iteration = self.hillclimber_counter

            HC4.schedule = self.schedule
            HC4.iteration = self.hillclimber_counter


            T = self.__set_temp(T)


            if mode == 'solo':
                activation = random.choice([1,2,3])

                if activation == 1:
                    HC1.schedule = self.schedule
                    HC1.iteration = self.hillclimber_counter

                    self.schedule, self.malus, self.hillclimber_counter = HC1.climb(T)


                    # print(self.malus)

                elif activation == 2:
                    HC2.schedule = self.schedule
                    HC2.iteration = self.hillclimber_counter

                    self.schedule, self.malus, self.hillclimber_counter = HC2.climb(T)


                    # print(self.malus)

                elif activation == 3:
                    HC3.schedule = self.schedule
                    HC3.iteration = self.hillclimber_counter

                    self.schedule, self.malus, self.hillclimber_counter = HC3.climb(T)


                    # print(self.malus)

                elif activation == 4:
                    HC4.schedule = self.schedule
                    HC4.iteration = self.hillclimber_counter
                    HC4.hillclimber_iterations = 1

                    self.schedule, self.malus, self.hillclimber_counter = HC4.climb(T)

                    # print(self.malus)
            elif mode == 'multi':

                core_assignment_list = [0,1,1,2]

                with Pool(4) as p:
                    self.output_schedules = p.map(self.run_HC, [(core_assignment_list[0], self.schedule, T, 1, self.hillclimber_counter),
                                                                (core_assignment_list[1], self.schedule, T, 2, self.hillclimber_counter),
                                                                (core_assignment_list[2], self.schedule, T, 3, self.hillclimber_counter),
                                                                (core_assignment_list[3], self.schedule, T, 4, self.hillclimber_counter)])
                # find the lowest malus of the output rosters
                min_malus = min([i[1]['Total'] for i in self.output_schedules])

                # Use the lowest malus to find the index of the best roster
                self.best_index = [i[1]['Total'] for i in self.output_schedules].index(min_malus)

                self.hillclimber_counter = self.output_schedules[0][3]

                # Compute difference between new roster and current roster
                difference = self.malus['Total'] - self.output_schedules[self.best_index][1]['Total']

                # replace the roster if it is better
                self.__replace_roster(difference)
                self.multiprocessor_counter += 1

            elif mode == 'genetic_pool':
                # genetic_schedules = [copy.deepcopy(self.schedule) for _ in range(32)]

                # with Pool(4) as p:
                #     self.output_schedules = p.map(self.run_HC, [(0, genetic_schedules[0], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[1], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[2], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[3], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[4], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[5], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[6], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[7], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[8], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[9], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[10], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[11], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[12], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[13], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[14], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[15], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[16], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[17], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[18], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[19], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[20], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[21], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[22], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[23], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[24], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[25], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[26], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[27], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[28], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[29], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[30], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[31], T, self.hillclimber_counter)])

                schedule1 = copy.deepcopy(self.schedule)
                schedule2 = copy.deepcopy(self.schedule)
                schedule3 = copy.deepcopy(self.schedule)
                schedule4 = copy.deepcopy(self.schedule)

                schedule_list = [schedule1, schedule2, schedule3, schedule4]

                while time.time() - start_time < 600:
                    total_output = []

                    for schedule in schedule_list:
                        for _ in range(2):
                            # print(f'before: {time.time() - start_time}')
                            with Pool(4) as p:
                                output_schedules = p.map(self.run_HC, [(0, schedule, T, self.hillclimber_counter),
                                                                            (1, schedule, T, self.hillclimber_counter),
                                                                            (2, schedule, T, self.hillclimber_counter),
                                                                            (3, schedule, T, self.hillclimber_counter)])
                            # print(f'after: {time.time() - start_time}')
                            total_output += output_schedules

                    # with Pool(4) as p:
                                # self.output_schedules = p.map(self.run_HC, [(0, schedules[0], T, self.hillclimber_counter),
                                #                                             (0, schedules[0], T, self.hillclimber_counter),
                                #                                             (0, schedules[1], T, self.hillclimber_counter),
                                #                                             (0, schedules[1], T, self.hillclimber_counter),
                                #                                             (0, schedules[2], T, self.hillclimber_counter),
                                #                                             (0, schedules[2], T, self.hillclimber_counter),
                                #                                             (0, schedules[3], T, self.hillclimber_counter),
                                #                                             (0, schedules[3], T, self.hillclimber_counter),
                                #                                             (1, schedules[0], T, self.hillclimber_counter),
                                #                                             (1, schedules[0], T, self.hillclimber_counter),
                                #                                             (1, schedules[1], T, self.hillclimber_counter),
                                #                                             (1, schedules[1], T, self.hillclimber_counter),
                                #                                             (1, schedules[2], T, self.hillclimber_counter),
                                #                                             (1, schedules[2], T, self.hillclimber_counter),
                                #                                             (1, schedules[3], T, self.hillclimber_counter),
                                #                                             (1, schedules[3], T, self.hillclimber_counter),
                                #                                             (2, schedules[0], T, self.hillclimber_counter),
                                #                                             (2, schedules[0], T, self.hillclimber_counter),
                                #                                             (2, schedules[1], T, self.hillclimber_counter),
                                #                                             (2, schedules[1], T, self.hillclimber_counter),
                                #                                             (2, schedules[2], T, self.hillclimber_counter),
                                #                                             (2, schedules[2], T, self.hillclimber_counter),
                                #                                             (2, schedules[3], T, self.hillclimber_counter),
                                #                                             (2, schedules[3], T, self.hillclimber_counter),
                                #                                             (3, schedules[0], T, self.hillclimber_counter),
                                #                                             (3, schedules[0], T, self.hillclimber_counter),
                                #                                             (3, schedules[1], T, self.hillclimber_counter),
                                #                                             (3, schedules[1], T, self.hillclimber_counter),
                                #                                             (3, schedules[2], T, self.hillclimber_counter),
                                #                                             (3, schedules[2], T, self.hillclimber_counter),
                                #                                             (3, schedules[3], T, self.hillclimber_counter),
                                #                                             (3, schedules[3], T, self.hillclimber_counter)])

                    random.shuffle(total_output)

                    populations = {}
                    for i, output in enumerate(total_output):
                        populations[i] = (output[0], output[1])

                    populations = self.tournament(populations)
                    for pop in populations:
                        print(time.time() - start_time)
                        print(populations[pop][1]['Total'])

                    schedule_list = [populations[value][0] for value in populations]

            elif mode == 'genetic':
                schedule1 = copy.deepcopy(self.schedule)
                schedule2 = copy.deepcopy(self.schedule)
                schedule3 = copy.deepcopy(self.schedule)
                schedule4 = copy.deepcopy(self.schedule)

                schedule_list = [schedule1, schedule2, schedule3, schedule4]

                while start_time - time.time() < 900:
                    total_output = []



                    for schedule in schedule_list:
                        for _ in range(2):
                            for i in range(4):
                                schedule, malus, _, _ = self.run_HC(i, schedule, T, self.hillclimber_counter)

                                total_output.append((schedule, malus))


                    random.shuffle(total_output)

                    populations = {}
                    for i, output in enumerate(total_output):
                        populations[i] = (output[0], output[1])

                    populations = self.tournament(populations)
                    for pop in populations:
                        print(time.time() - start_time)
                        print(populations[pop][1]['Total'])

                    schedule_list = [populations[value][0] for value in populations]

    def tournament(self, populations) -> dict:
        while len(populations) > 4:
            new_populations = {}
            counter = 0
            for i in range(0, len(populations.keys()), 2):
                if populations[i][1]['Total'] < populations[i+1][1]['Total']:
                    new_populations[counter] = populations[i]
                else:
                    new_populations[counter] = populations[i+1]
                counter += 1

            populations = new_populations
        return populations

    def run(self):

        # Set Initial variable
        self.multiprocessor_counter = 0
        self.hillclimber_counter = 0
        self.fail_counter = 0
        self.duration = 0

        self.schedule = self.Roster.schedule

        self.malus = self.MC.compute_total_malus(self.schedule)

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        if self.ANNEALING:
            t = .8
        else:
            t = 0

        core_assignment_list = [0,0,0,0]


        while self.fail_counter != 10:

            if self.ANNEALING:
                if t > .5:
                    t = self.__get_temperature(t)
                elif t <= 0.5:
                    t = self.__get_temperature(t, alpha=0.65)

                if t < 0.01:
                    t = 0.05
            else:
                t = 0


            if self.malus['Capacity'] < 15:
                core_assignment_list = [0,1,2,3]

            start_time = time.time()

            # Fill the pool with all functions and their rosters
            with Pool(4) as p:
                self.output_schedules = p.map(self.run_HC, [(core_assignment_list[0], self.schedule, t, 1, self.hillclimber_counter),
                                                            (core_assignment_list[1], self.schedule, t, 2, self.hillclimber_counter),
                                                            (core_assignment_list[2], self.schedule, t, 3, self.hillclimber_counter),
                                                            (core_assignment_list[3], self.schedule, t, 4, self.hillclimber_counter)])

            # find the lowest malus of the output rosters
            min_malus = min([i[1]['Total'] for i in self.output_schedules])

            # Use the lowest malus to find the index of the best roster
            self.best_index = [i[1]['Total'] for i in self.output_schedules].index(min_malus)

            self.hillclimber_counter = self.output_schedules[0][3]

            # Compute difference between new roster and current roster
            difference = self.malus['Total'] - self.output_schedules[self.best_index][1]['Total']

            # Set finish time
            finish_time = time.time()

            self.multiprocess_duration = finish_time - start_time
            self.duration += self.multiprocess_duration

            # replace the roster if it is better
            self.__replace_roster(difference)

            self.multiprocessor_counter += 1

        self.finish()

    def run_solo(self):

        # Set counters
        self.fail_counter = 0
        self.multiprocessor_counter = 0
        self.hillclimber_counter = 0
        self.duration = 0

        self.schedule = self.Roster.schedule

        self.malus = self.MC.compute_total_malus(self.schedule)

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)
        if self.ANNEALING:
            t = .8
        else:
            t = 0

        while self.fail_counter != 300000:

            start_time = time.time()

            if self.ANNEALING:
                if t > .5:
                    t = self.__get_temperature(t)
                elif t <= 0.5:
                    t = self.__get_temperature(t, alpha=0.65)

                if t < 0.01:
                    t = 0.05
            else:
                t = 0

            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter)
            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter)
            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter)
            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter)

            if self.malus['Total'] > 200:
                self.schedule, malus, iteration = HC1.climb(t)

            else:
                activation = random.choice([1,3])
                if activation == 1:
                    self.schedule, malus, iteration = HC1.climb(t)
                if activation == 2:
                    self.schedule, malus, iteration = HC2.climb(t)
                if activation == 3:
                    self.schedule, malus, iteration = HC3.climb(t)
                if activation == 4:
                    self.schedule, malus, iteration = HC4.climb(t)

            self.hillclimber_counter = iteration

            # Compute difference between new roster and current roster
            difference = self.malus['Total'] - malus['Total']

            self.malus = malus

            # Set finish time
            finish_time = time.time()

            self.multiprocess_duration = finish_time - start_time
            self.duration += self.multiprocess_duration

            # replace the roster if it is better
            self.__replace_roster(difference)

            self.multiprocessor_counter += 1

        self.finish()

    def finish(self):

        with open('data/terminate.txt', 'w') as f:
                f.write('True')

        app = SelectorApp.App(self.student_list, self.schedule)
        app.mainloop()

    def run_HC(self, hc_tuple):
        activation, schedule, T, iteration = hc_tuple
        if activation == 0:

            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(schedule, self.course_list, self.student_list, self.MC, iteration)
            schedule, malus, iteration = HC1.climb(T)

            return schedule, malus, HC1.get_name(), iteration

        elif activation == 1:

            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(schedule, self.course_list, self.student_list, self.MC, iteration)
            schedule, malus, iteration = HC2.climb(T)

            return schedule, malus, HC2.get_name(), iteration

        elif activation == 2:

            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(schedule, self.course_list, self.student_list, self.MC, iteration)
            schedule, malus, iteration = HC3.climb(T)

            return schedule, malus, HC3.get_name(), iteration

        elif activation == 3:

            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(schedule, self.course_list, self.student_list, self.MC, iteration)
            schedule, malus, iteration = HC4.climb(T)

            return schedule, malus, HC4.get_name(), iteration

    def __get_temperature(self, t, alpha=0.995):
        """Exponential decay temperature schedule"""
        return t*alpha

    def __replace_roster(self, difference):

        # If difference is positive
        if difference >= 0:

            # Set the new roster to self.Roster
            self.schedule, self.malus, _, _ = self.output_schedules[self.best_index]
            self.fail_counter = 0

            # print(f'\n========================= Generation: {self.multiprocessor_counter} =========================\n')
            # print(f'Most effective function: HC{name}')
            # print(f'Malus improvement: {difference}')
            # print(f'Duration of iteration: {round(self.multiprocess_duration, 2)} S.')
            # print(f'Duration since init: {round(self.duration, 2)} S.')
            # print(self.malus)

        else:
            self.fail_counter += 1
            print(f'Fails: {self.fail_counter}')

            # print output
            # print(f'\n========================= Generation: {self.multiprocessor_counter} =========================\n')
            # print('FAIL')
            # print(f'Duration of iteration: {round(self.multiprocess_duration, 2)} S.')
            # print(f'Duration since init: {round(self.duration, 2)} S.')
            # print(self.malus)

class Multiprocessor_SimAnnealing(Multiprocessor):

    def __replace_roster(self, difference):
        # set the temperature
        T = (150/(200 + self.multiprocessor_counter*2))

        # If difference is positive
        if difference > 0:

            # Set the new roster to self.Roster
            self.schedule, self.malus, name, _ = self.output_schedules[self.best_index]
            print(self.best_index)
            self.fail_counter = 0

            print(f'\n========================= Generation: {self.multiprocessor_counter} =========================\n')
            print(f'Most effective function: HC{name}')
            print(f'Malus improvement: {difference}')
            print(f'Duration of iteration: {round(self.multiprocess_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)

        else:
            self.fail_counter += 1

            # print output
            print(f'\n========================= Generation: {self.multiprocessor_counter} =========================\n')
            print('FAIL')
            print(f'Duration of iteration: {round(self.multiprocess_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)

class Multiprocessor_SimAnnealing(Multiprocessor):

    def __replace_roster(self, difference):
        # set the temperature
        T = (150/(200 + self.multiprocessor_counter*2))

        # If difference is positive
        if difference > 0:

            # Set the new roster to self.Roster
            self.schedule, self.malus, _ = self.output_schedules[self.best_index]
            self.fail_counter = 0

            print(f'\n========================= Generation: {self.multiprocessor_counter} =========================\n')
            print(f'Temperature at generation: {T}')
            print(f'Most effective function: SA{self.best_index + 1}')
            print(f'Malus improvement: {difference}')
            print(f'Duration of iteration: {round(self.multiprocess_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)

        elif difference < 0:
            prob = random.random()
            if prob < T:
                self.schedule, self.malus = random.choice(self.output_schedules)
                self.fail_counter = 0

                # print output
                print(f'\n========================= Generation: {self.multiprocessor_counter} =========================\n')
                print(f'FAIL GOT ACCEPTED WITH TEMPERATURE AT: {T}')
                print(f'Duration of iteration: {round(self.multiprocess_duration, 2)} S.')
                print(f'Duration since init: {round(self.duration, 2)} S.')
                print(self.malus)

            else:
                self.fail_counter += 1

                # print output
                print(f'\n========================= Generation: {self.multiprocessor_counter} =========================\n')
                print('FAIL')
                print(f'Duration of iteration: {round(self.multiprocess_duration, 2)} S.')
                print(f'Duration since init: {round(self.duration, 2)} S.')
                print(self.malus)