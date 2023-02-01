import classes.algorithms.hillclimber as HillCLimberClass
from multiprocessing import Pool
import random
from helpers.shallow_copy import recursive_copy
from data.assign import student_list, course_list
import classes.representation.malus_calc as MalusCalculatorClass

import pickle
import time
import csv


class Multiprocessor():
    def __init__(self, Roster, annealing, experiment_iter):
        self.Roster = Roster
        self.course_list = course_list
        self.student_list = student_list
        self.ITERS = 1
        self.ANNEALING = annealing
        self.experiment_iter = experiment_iter

        self.MC = MalusCalculatorClass.MC()

    def __init_temp(self) -> float:
        if self.ANNEALING:
            return 1
        else:
            return 0

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

    """ Multiprocessing """

    def run_multi(self, algorithm_duration, experiment, core_assignment, hill_climber_iters):

        self.data = []

        # Set counters
        self.multiprocess_iter_counter = 0
        self.hillclimber_iter_counter = 0
        self.fail_counter = 0
        self.duration = 0

        lowest_malus = 9999

        self.schedule = self.Roster.schedule
        self.malus = self.MC.compute_total_malus(self.schedule)

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)
        if self.ANNEALING:
            t = 1
        else:
            t = 0

        init_time = time.time()

        # while self.Roster.malus_cause['Dubble Classes'] != 0 or self.Roster.malus_cause['Capacity'] != 0:
        while time.time() - init_time < algorithm_duration:
        # while self.iter_counter != 2:

            start_time = time.time()

            # Increase iter counter
            self.multiprocess_iter_counter += 1

            self.malus = self.MC.compute_total_malus(self.schedule)

            schedule_list = [recursive_copy(self.schedule) for _ in range(4)]

            # Fill the pool with all functions and their rosters
            with Pool(4) as p:
                self.output_schedules = p.map(self.run_HC, [(core_assignment[0], schedule_list[0], t, self.hillclimber_iter_counter, hill_climber_iters),
                                                            (core_assignment[1], schedule_list[1], t, self.hillclimber_iter_counter, hill_climber_iters),
                                                            (core_assignment[2], schedule_list[2], t, self.hillclimber_iter_counter, hill_climber_iters),
                                                            (core_assignment[3], schedule_list[3], t, self.hillclimber_iter_counter, hill_climber_iters)])

            # find the lowest malus of the output rosters
            min_malus = min([i[1]['Total'] for i in self.output_schedules])

            # Use the lowest malus to find the index of the best roster
            self.best_index = [i[1]['Total'] for i in self.output_schedules].index(min_malus)

            # Compute difference between new roster and current roster
            difference = self.malus['Total'] - self.output_schedules[self.best_index][1]['Total']

            if self.output_schedules[self.best_index][1]['Total'] < lowest_malus:
                lowest_malus = self.output_schedules[self.best_index][1]['Total']
                self.save_schedule(self.output_schedules[self.best_index][0])

            finish_time = time.time()

            self.iter_duration = finish_time - start_time
            self.duration += self.iter_duration

            # replace the roster if it is better
            self.__replace_roster(difference)

            for output_schedule in self.output_schedules:
                self.save_data_multi(output_schedule[2], output_schedule[1]['Total'], self.multiprocess_iter_counter, round(self.duration, 2))


        self.export_data_multi(experiment)


    def save_data_multi(self, HC_name, cost, iteration, time):
        self.data.append({'Hill Climber': HC_name, 'Cost': cost, 'Iteration': iteration, 'Duration': time})

    def export_data_multi(self, experiment):
        fields = ['Hill Climber', 'Cost', 'Iteration', 'Duration']

        with open(f'data/experiment{experiment}.csv', 'a', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fields)

            if self.experiment_iter == 0:
                csv_writer.writeheader()

            for row in self.data:
                csv_writer.writerow(row)

    """ Genetic """

    def run_genetic(self, algorithm_duration, experiment):

        # Set Initial variable
        self.fail_counter = 0
        self.hillclimber_iter_counter = 1
        self.data = []
        self.schedule = self.Roster.schedule
        self.malus = self.MC.compute_total_malus(self.schedule)

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        first_stage_start_time = time.time()

        """ First Stage """

        T = self.__init_temp()

        while self.malus['Total'] > 125:
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(self.schedule, self.hillclimber_iter_counter)
            self.schedule, self.malus, self.hillclimber_counter, _ = HC1.climb()
            print(self.malus)

        first_stage_duration = time.time() - first_stage_start_time

        print(f'\nFirst stage duration: {round(first_stage_duration, 2)} Seconds\n')


        """ Second Stage """

        second_stage_start_time = time.time()

        # when annealing, if the worsening did not make it better in the long run, return to best schedule
        counter_since_improvement = 0
        best_score = 1000
        best_schedule = None
        if self.ANNEALING:
            T *= 0.995

        self.save_data_genetic(0, time.time() - second_stage_start_time, self.malus['Total'])

        schedule_list = [recursive_copy(self.schedule) for _ in range(4)]

        while time.time() - second_stage_start_time < algorithm_duration:

            total_output = []

            counter_since_improvement += 1

            if self.ANNEALING:
                # if sim annealing worsening did not result in long run improvements, return to old state
                if counter_since_improvement > 3000:
                    schedule_list = [recursive_copy(best_schedule) for _ in range(4)]

            # flag variable to stop running one iteration if a sim annealing worsening happened
            accepted = False
            for schedule_index, schedule in enumerate(schedule_list):
                for _ in range(2):
                    for i in range(4):
                        schedule, malus, _, _, accept_me = self.run_HC((i, schedule, T, 0, 1))
                        if accept_me:

                            # if this is the new schedule, make a data entry for every one of the 4 schedules
                            for i in range(4):
                                self.save_data_genetic(i, time.time(), malus['Total'])

                            schedule_list = [schedule, schedule, schedule, schedule]
                            accepted = True
                            self.fail_counter = 0
                            continue

                        # Append result to output list
                        total_output.append((schedule, malus))

            # Continue if accepted is True
            if accepted:
                continue

            # Randomize total output list
            random.shuffle(total_output)

            # Create populations dict
            populations = {}

            # for each output:
            for i, output in enumerate(total_output):

                # Create a key with schedule and malus as value
                populations[i] = (output[0], output[1])

            # Select best four schedules
            populations = self.tournament(populations)

            for i, pop in enumerate(populations):

                # Save the data of each surviving schedule
                self.save_data_genetic(i, time.time(), populations[pop][1]['Total'])

                # If new malus is better than pior best malus
                if populations[pop][1]['Total'] < best_score:

                    # Set new schedule and malus
                    best_score = populations[pop][1]['Total']
                    best_schedule = populations[pop][0]

                    # Save the schedule
                    self.save_schedule(best_schedule)

                    # Reset counters
                    counter_since_improvement = 0
                    self.fail_counter = 0
                else:
                    self.fail_counter += 1

            schedule_list = [populations[value][0] for value in populations]

        self.export_data_genetic(experiment)

    def run_genetic_pool(self, algorithm_duration, experiment, core_assignment, hill_climber_iters):

        # Set Initial variable
        self.multiprocessor_counter = 0
        self.hillclimber_counter = 0
        self.fail_counter = 0
        self.duration = 0

        # Set a very high lowest malus
        lowest_malus = 9999

        self.data = []

        self.schedule = self.Roster.schedule
        self.malus = self.MC.compute_total_malus(self.schedule)

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        first_stage_start_time = time.time()

        """ First Stage """

        t = self.__init_temp()

        while self.malus['Capacity'] > 15:
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(self.schedule, self.hillclimber_counter)
            self.schedule, self.malus, self.hillclimber_counter, _ = HC1.climb()
            print(self.malus)

        first_stage_duration = time.time() - first_stage_start_time

        print(f'\nFirst stage duration: {round(first_stage_duration, 2)} Seconds\n')


        """ Second Stage """

        second_stage_start_time = time.time()

        self.save_data_genetic(0, time.time() - second_stage_start_time, self.malus['Total'])

        schedule_list = [recursive_copy(self.schedule) for _ in range(4)]

        while time.time() - second_stage_start_time < algorithm_duration:

            total_output = []
            for schedule in schedule_list:
                with Pool(4) as p:
                    output_schedules = p.map(self.run_HC, [(core_assignment[0], schedule, t, self.hillclimber_counter, hill_climber_iters),
                                                                (core_assignment[1], schedule, t, self.hillclimber_counter, hill_climber_iters),
                                                                (core_assignment[2], schedule, t, self.hillclimber_counter, hill_climber_iters),
                                                                (core_assignment[3], schedule, t, self.hillclimber_counter, hill_climber_iters)])

                total_output += output_schedules

            # Randomize total output list
            random.shuffle(total_output)

            populations = {}
            for i, output in enumerate(total_output):
                populations[i] = (output[0], output[1])

            populations = self.tournament(populations)

            for i, pop in enumerate(populations):
                self.save_data_genetic(i, time.time() - second_stage_start_time, populations[pop][1]['Total'])

            schedule_list = [populations[value][0] for value in populations]

            for pop in populations:
                if populations[pop][1]['Total'] < lowest_malus:
                    lowest_malus = populations[pop][1]['Total']
                    self.save_schedule(populations[pop][0])

        self.export_data_genetic(experiment)


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

    def save_data_genetic(self, schedule_index, time, cost) -> None:
        self.data.append({'Schedule Index': schedule_index, 'Duration': time, 'Cost': cost})

    def export_data_genetic(self, experiment) -> None:
        fields = ['Schedule Index', 'Duration', 'Cost']
        with open(f'data/experiment{experiment}.csv', 'a', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fields)

            if self.experiment_iter == 0:
                csv_writer.writeheader()
            for row in self.data:
                csv_writer.writerow(row)

    """ Sequential """

    def run_solo(self, algorithm_duration, experiment):

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

        # Set starting time for the process
        process_start_time = time.time()

        # while time is smaller than input duration
        while time.time() - process_start_time < algorithm_duration:

            # Set start time for iteration
            iteration_start_time = time.time()

            if self.ANNEALING:
                if t > .5:
                    t = self.__get_temperature(t)
                elif t <= 0.5:
                    t = self.__get_temperature(t, alpha=0.65)

                if t < 0.01:
                    t = 0.05
            else:
                t = 0

            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(self.schedule, self.hillclimber_counter)
            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(self.schedule, self.hillclimber_counter)
            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(self.schedule, self.hillclimber_counter)
            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(self.schedule, self.hillclimber_counter)

            if self.malus['Total'] > 200:
                schedule, malus, iteration = HC1.climb(t)

            else:
                activation = random.choice([1,2,3,4])
                if activation == 1:
                    schedule, malus, iteration = HC1.climb(t)
                if activation == 2:
                    schedule, malus, iteration = HC2.climb(t)
                if activation == 3:
                    schedule, malus, iteration = HC3.climb(t)
                if activation == 4:
                    schedule, malus, iteration = HC4.climb(t)

            self.hillclimber_counter = iteration

            # Compute difference between new roster and current roster
            difference = self.malus['Total'] - malus['Total']

            # If new malus is smaller than set malus
            if malus['Total'] < self.malus['Total']:

                # Save the schedule
                self.save_schedule(schedule)

                # Set schedule to self
                self.schedule = schedule

                self.malus = malus

            # Set finish time
            finish_time = time.time()

            self.multiprocess_duration = finish_time - iteration_start_time
            self.duration += self.multiprocess_duration

            # replace the roster if it is better
            self.__replace_roster(difference)

            self.multiprocessor_counter += 1

    def run_HC(self, hc_tuple):
        activation, schedule, T, iteration, hill_climber_iters = hc_tuple
        if activation == 0:

            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(schedule, iteration)
            schedule, malus, iteration, accept_me = HC1.climb(hill_climber_iters, T=T, ANNEALING=self.ANNEALING, fail_counter=self.fail_counter)

            return schedule, malus, HC1.get_name(), iteration, accept_me

        elif activation == 1:

            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(schedule, iteration)
            schedule, malus, iteration, accept_me = HC2.climb(hill_climber_iters, T=T, ANNEALING=self.ANNEALING, fail_counter=self.fail_counter)

            return schedule, malus, HC2.get_name(), iteration, accept_me

        elif activation == 2:

            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(schedule, iteration)
            schedule, malus, iteration, accept_me = HC3.climb(hill_climber_iters, T=T, ANNEALING=self.ANNEALING, fail_counter=self.fail_counter)

            return schedule, malus, HC3.get_name(), iteration, accept_me

        elif activation == 3:

            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(schedule, iteration)
            schedule, malus, iteration, accept_me = HC4.climb(hill_climber_iters, T=T, ANNEALING=self.ANNEALING, fail_counter=self.fail_counter)

            return schedule, malus, HC4.get_name(), iteration, accept_me

    def __get_temperature(self, t, alpha=0.995):
        """Exponential decay temperature schedule"""
        return t*alpha

    def __replace_roster(self, difference):

        # If difference is positive
        if difference >= 0:

            # Set the new roster to self.Roster
            self.schedule, self.malus, _, _, _ = self.output_schedules[self.best_index]
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

    def save_schedule(self, schedule):
        with open('schedule.pkl', 'wb') as f:
            pickle.dump(schedule, f)