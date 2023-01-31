import classes.algorithms.hillclimber as HillCLimberClass
from multiprocessing import Pool
import random
import classes.GUI.selector_GUI as SelectorApp
from helpers.shallow_copy import recursive_copy

import time


class Multiprocessor():
    def __init__(self, Roster, course_list, student_list, MC, annealing):
        self.Roster = Roster
        self.course_list = course_list
        self.student_list = student_list
        self.ITERS = 1
        self.ANNEALING = annealing

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

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        hillclimb_iters = 1000

        start_time = time.time()

        while self.malus['Total'] > 150:

            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter, hillclimb_iters)
            self.schedule, self.malus, self.hillclimber_counter = HC1.climb(T)
            HC1.schedule = self.schedule
            HC1.iteration = self.hillclimber_counter

            print(self.malus)

        # Initialize all hillclimbers
        
        # HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter, hillclimb_iters)
        # HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter, hillclimb_iters)
        # HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter, hillclimb_iters)


        # HC2.schedule = self.schedule
        # HC2.iteration = self.hillclimber_counter

        # HC3.schedule = self.schedule
        # HC3.iteration = self.hillclimber_counter

        # HC4.schedule = self.schedule
        # HC4.iteration = self.hillclimber_counter


        T = self.__set_temp(T)

        hillclimb_iters = 250

        if mode == 'multi':

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

            schedule_list = [recursive_copy(self.schedule) for _ in range(4)]

            while time.time() - start_time < 900:

                gen_time_start = time.time()

                total_output = []
                for schedule in schedule_list:
                    print(f'before: {time.time() - gen_time_start}')
                    with Pool(4) as p:
                        output_schedules = p.map(self.run_HC, [(0, schedule, T, self.hillclimber_counter, hillclimb_iters),
                                                                    (1, schedule, T, self.hillclimber_counter, hillclimb_iters),
                                                                    (2, schedule, T, self.hillclimber_counter, hillclimb_iters),
                                                                    (3, schedule, T, self.hillclimber_counter, hillclimb_iters)])
                    print(f'after: {time.time() - gen_time_start}')
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
                    print(time.time() - gen_time_start)
                    print(populations[pop][1]['Total'])

                schedule_list = [populations[value][0] for value in populations]

        elif mode == 'genetic':

                schedule_list = [recursive_copy(self.schedule) for _ in range(4)]

                while time.time() - start_time < 900:

                    gen_time_start = time.time()

                    total_output = []
                    for schedule in schedule_list:
                        for _ in range(2):
                            for i in range(4):
                                schedule, malus, _, _ = self.run_HC((i, schedule, T, self.hillclimber_counter))

                                total_output.append((schedule, malus))


                    random.shuffle(total_output)

                    populations = {}
                    for i, output in enumerate(total_output):
                        populations[i] = (output[0], output[1])

                    populations = self.tournament(populations)
                    for pop in populations:
                        print(time.time() - gen_time_start)
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

        first_stage_start_time = time.time()

        """ First Stage """

        t = self.__init_temp()

        while self.malus['Capacity'] > 15:
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(self.schedule, self.course_list, self.student_list, self.MC, self.hillclimber_counter)
            self.schedule, self.malus, self.hillclimber_counter = HC1.climb(t)
            print(self.malus)

        first_stage_duration = time.time() - first_stage_start_time

        print(f'\nFirst stage duration: {round(first_stage_duration, 2)} Seconds\n')


        """ Second Stage """

        second_stage_start_time = time.time()

        schedule_list = [recursive_copy(self.schedule) for _ in range(4)]

        while time.time() - second_stage_start_time < 1:

            gen_time_start = time.time()

            total_output = []
            for schedule in schedule_list:
                # for _ in range (2):
                    print(f'before: {time.time() - gen_time_start}')

                    with Pool(4) as p:
                        output_schedules = p.map(self.run_HC, [(0, schedule, t, self.hillclimber_counter),
                                                                    (0, schedule, t, self.hillclimber_counter),
                                                                    (2, schedule, t, self.hillclimber_counter),
                                                                    (2, schedule, t, self.hillclimber_counter)])

                    print(f'after: {time.time() - gen_time_start}')
                    total_output += output_schedules

            random.shuffle(total_output)

            populations = {}
            for i, output in enumerate(total_output):
                populations[i] = (output[0], output[1])

            populations = self.tournament(populations)
            for pop in populations:
                print(time.time() - gen_time_start)
                print(populations[pop][1]['Total'])

            schedule_list = [populations[value][0] for value in populations]

        lowest_malus = 9999
        for pop in populations:
            if populations[pop][1]['Total'] < lowest_malus:
                lowest_malus = populations[pop][1]['Total']
                self.schedule = populations[pop][0]

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