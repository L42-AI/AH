import classes.algorithms.hillclimber as HillCLimberClass
from multiprocessing import Pool
import random
from data.assign import student_list, course_list
import classes.representation.malus_calc as MalusCalculatorClass

import pickle
import time
import csv


class Optimize():
    '''
    This class runs different types of algorithms on a given schedule. It can run Hillclimbers
    independent of each other, use a genetic algorithm and or simmulated annealing. README in 
    the git for more detail
    '''

    def __init__(self, Roster, annealing, experiment_iter):
        self.Roster = Roster
        self.course_list = course_list
        self.student_list = student_list
        self.ITERS = 1
        self.ANNEALING = annealing
        self.experiment_iter = experiment_iter

        self.MC = MalusCalculatorClass.MC()

    def __init_temp(self) -> float:
        '''Sets the temperature to 1 to start simmulated annealing if simulated annealing is selected'''

        if self.ANNEALING:
            return 1
        else:
            return 0

    """ Sequential """

    def run_solo(self, algorithm_duration, experiment, core_assignment, hill_climber_iters):

        # Set initial schedule and malus
        self.schedule = self.Roster.schedule
        self.malus = self.MC.compute_total_malus(self.schedule)

        # Set counters
        self.multiprocessor_counter = 0
        self.hillclimber_counter = 0
        self.fail_counter = 0
        self.duration = 0

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        t = self.__init_temp()

        # Set starting time for the process
        process_start_time = time.time()

        # While time is smaller than input duration
        while time.time() - process_start_time < algorithm_duration:

            # Set start time for iteration
            iteration_start_time = time.time()

            # Initiate the hillclimbers
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(self.schedule, self.hillclimber_counter)
            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(self.schedule, self.hillclimber_counter)
            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(self.schedule, self.hillclimber_counter)
            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(self.schedule, self.hillclimber_counter)

            # Run hill climber 1 if malus is larger than 125
            if self.malus['Total'] > 125:
                schedule, malus, iteration, _ = HC1.climb(hill_climber_iters)

            else:
                # Randomize activation from core assignment
                activation = random.choice(core_assignment)

                # Run hill climber
                if activation == 1:
                    schedule, malus, iteration = HC1.climb(hill_climber_iters)
                elif activation == 2:
                    schedule, malus, iteration = HC2.climb(hill_climber_iters)
                elif activation == 3:
                    schedule, malus, iteration = HC3.climb(hill_climber_iters)
                elif activation == 4:
                    schedule, malus, iteration = HC4.climb(hill_climber_iters)

            # Set the iteration
            self.hillclimber_counter += iteration

            # Compute difference between new roster and current roster
            difference = self.malus['Total'] - malus['Total']

            # If new malus is smaller than set malus
            if malus['Total'] < self.malus['Total']:

                # Save the schedule
                self.save_schedule(schedule)

                # Set schedule to self
                self.schedule = schedule

                # Set malus to self
                self.malus = malus

            # Set finish time
            finish_time = time.time()

            # record the time
            self.multiprocess_duration = finish_time - iteration_start_time
            self.duration += self.multiprocess_duration

            # replace the roster if it is better and print output
            self.__replace_roster(difference)

            self.multiprocessor_counter += 1


    """ Multiprocessing """

    def run_multi(self, algorithm_duration, experiment, core_assignment, hill_climber_iters):
        """
        This method can run any combination of our 4 Hillclimbing algorithms. Every iteration,
        a Hillclimber is called upon 4 times. Since each Hillclimber works independent, the task can
        be split up to run on multiple cores. Only advised to do when choosing high iterations per Hillclimber.
        read README on git for more info
        """

        self.data = []
        init_time = time.time()

        # Set counters
        self.multiprocess_iter_counter = 0
        self.hillclimber_iter_counter = 0
        self.fail_counter = 0
        self.duration = 0

        # set a 'lowest' malus
        lowest_malus = 9999

        # self.schedule and self.malus will always hold the best schedule
        self.schedule = self.Roster.schedule
        self.malus = self.MC.compute_total_malus(self.schedule)

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        # set a temperature dependend on simulated annealing or not
        t = self.__init_temp()

        # run for a given amount of time
        while time.time() - init_time < algorithm_duration:
            start_time = time.time()

            # Increase iter counter
            self.multiprocess_iter_counter += 1

            # set schedules and malus for the next iteration
            self.malus = self.MC.compute_total_malus(self.schedule)
            schedule_list = [self.recursive_copy(self.schedule) for _ in range(4)]

            # Fill the pool with all functions and their rosters
            with Pool(4) as p:
                output_schedules = p.map(self.run_HC, [(core_assignment[0], schedule_list[0], t, hill_climber_iters),
                                                            (core_assignment[1], schedule_list[1], t, hill_climber_iters),
                                                            (core_assignment[2], schedule_list[2], t, hill_climber_iters),
                                                            (core_assignment[3], schedule_list[3], t, hill_climber_iters)])

            # find the lowest malus of the output rosters
            min_malus = min([i[1]['Total'] for i in output_schedules])

            # Use the lowest malus to find the index of the best roster
            self.best_index = [i[1]['Total'] for i in output_schedules].index(min_malus)

            # Compute difference between new roster and current roster
            difference = self.malus['Total'] - output_schedules[self.best_index][1]['Total']


            if output_schedules[self.best_index][1]['Total'] < lowest_malus:
                lowest_malus = output_schedules[self.best_index][1]['Total']
                self.save_schedule(output_schedules[self.best_index][0])

            finish_time = time.time()

            self.iter_duration = finish_time - start_time
            self.duration += self.iter_duration

            # replace the roster if it is better
            self.__replace_roster(difference)

            for output_schedule in output_schedules:
                self.save_data_multi(output_schedule[2], output_schedule[1]['Total'], self.multiprocess_iter_counter, round(self.duration, 2))


        self.export_data_multi(experiment)


    def save_data_multi(self, HC_name, cost, iteration, time):
        """
        This function saves the data made in run_multi
        """
        self.data.append({'Hill Climber': HC_name, 'Cost': cost, 'Iteration': iteration, 'Duration': time})

    def export_data_multi(self, experiment):
        """
        This function exports the data collected in multi to a csv
        """

        # Set headers
        fields = ['Hill Climber', 'Cost', 'Iteration', 'Duration']

        # Open the csv
        with open(f'data/experiment{experiment}.csv', 'a', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fields)

            # Only write the headers on first iterations
            if self.experiment_iter == 0:
                csv_writer.writeheader()

            # Add all data
            for row in self.data:
                csv_writer.writerow(row)

    """ Genetic """

    def run_genetic(self, algorithm_duration, experiment):
        """
        This method runs hillclimber 0 and afterwards starts a genetic algorithm,
        which runs all 4 Hillclimbing algorithms for a total of 32 hillclimbing opperations
        read README on git for more info
        """

        """ Init """

        # Set initial schedule and malus
        self.schedule = self.Roster.schedule
        self.malus = self.MC.compute_total_malus(self.schedule)

        # Set Initial variable
        self.hillclimber_iter_counter = 1
        self.fail_counter = 0
        self.data = []

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        """ First Stage """

        first_stage_start_time = time.time()

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

        schedule_list = [self.recursive_copy(self.schedule) for _ in range(4)]

        while time.time() - second_stage_start_time < algorithm_duration:

            total_output = []

            counter_since_improvement += 1

            if self.ANNEALING:
                # if sim annealing worsening did not result in long run improvements, return to old state
                if counter_since_improvement > 3000:
                    schedule_list = [self.recursive_copy(best_schedule) for _ in range(4)]

            # flag variable to stop running one iteration if a sim annealing worsening happened
            accepted = False
            for schedule in enumerate(schedule_list):
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

            # Select four schedules with lowest malus
            populations = self.tournament(populations)

            # For each surviving schedule:
            for i, pop in enumerate(populations):

                # Save data
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
                    # Increase counter
                    self.fail_counter += 1

            # Make list of surviving schedules
            schedule_list = [populations[value][0] for value in populations]

        # Export data
        self.export_data_genetic(experiment)

    def run_genetic_pool(self, algorithm_duration, experiment, core_assignment, hill_climber_iters):
        """
        This method runs hillclimber 0 and afterwards starts a genetic algorithm,
        which runs all 4 Hillclimbing algorithms for a total of 32 hillclimbing opperations.
        This is done using multiproccessing with a pool of 4 read README on git for more info
        """

        """ Init """

        # Set Initial variable
        self.hillclimber_counter = 0
        self.fail_counter = 0
        self.duration = 0

        # Set a very high lowest malus
        lowest_malus = 9999

        # Create list to record data
        self.data = []

        # Set the initial schedule and malus
        self.schedule = self.Roster.schedule
        self.malus = self.MC.compute_total_malus(self.schedule)

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)

        """ First Stage """

        # Set starting time first stage
        first_stage_start_time = time.time()

        # Set temperature for annealing
        t = self.__init_temp()

        # While the total malus is over 125:
        while self.malus['Total'] > 125:

            # Create the first hillclimber
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(self.schedule, self.hillclimber_counter)

            # Do a climb iteration
            self.schedule, self.malus, self.hillclimber_counter, _ = HC1.climb(hill_climber_iters)

            # Visualize malus
            print(self.malus)

        # Calculate duration of first stage
        first_stage_duration = time.time() - first_stage_start_time

        # Visualize duration
        print(f'\nFirst stage duration: {round(first_stage_duration, 2)} Seconds\n')


        """ Second Stage """

        # Set starting time second stage
        second_stage_start_time = time.time()

        # Save the initial state
        self.save_data_genetic(0, time.time() - second_stage_start_time, self.malus['Total'])

        # Make a list of four copies of the schedule
        schedule_list = [self.recursive_copy(self.schedule) for _ in range(4)]

        # While the given duration is not achieved
        while time.time() - second_stage_start_time < algorithm_duration:

            # Create a total output list
            total_output = []

            # For each schedule
            for schedule in schedule_list:
                for _ in range(2):
                    # Run multicore with all settings
                    with Pool(4) as p:
                        output_schedules = p.map(self.run_HC, [(core_assignment[0], schedule, t, self.hillclimber_counter, hill_climber_iters),
                                                                    (core_assignment[1], schedule, t, self.hillclimber_counter, hill_climber_iters),
                                                                    (core_assignment[2], schedule, t, self.hillclimber_counter, hill_climber_iters),
                                                                    (core_assignment[3], schedule, t, self.hillclimber_counter, hill_climber_iters)])

                    # Add this output to the total output list
                    total_output += output_schedules

            # Randomize total output list
            random.shuffle(total_output)

            # Create populations dict
            populations = {}

            # For each output:
            for i, output in enumerate(total_output):
                # Create a key with schedule and malus as value
                populations[i] = (output[0], output[1])

            # Select four schedules with lowest malus
            populations = self.tournament(populations)

            # For each surviving schedule:
            for i, pop in enumerate(populations):

                # Save data
                self.save_data_genetic(i, time.time() - second_stage_start_time, populations[pop][1]['Total'])

                # If new malus is better than pior best malus
                if populations[pop][1]['Total'] < lowest_malus:

                    # Set new malus
                    lowest_malus = populations[pop][1]['Total']

                    # Save the schedule
                    self.save_schedule(populations[pop][0])

            # Make list of surviving schedules
            schedule_list = [populations[value][0] for value in populations]

        # Export data
        self.export_data_genetic(experiment)


    def tournament(self, populations) -> dict:
        """
        This function creates a knockout tournament,
        where the best schedule is selecte in sets of two
        """
        # While the population is greater than 4
        while len(populations) > 4:

            # Set dict for new population
            new_populations = {}

            # Set a counter
            index = 0

            # For each schedule in sets:
            for i in range(0, len(populations.keys()), 2):

                # Set the schedule with the lowest malus in the new dict
                if populations[i][1]['Total'] < populations[i+1][1]['Total']:
                    new_populations[index] = populations[i]
                else:
                    new_populations[index] = populations[i+1]

                # Increase index
                index += 1

            # Set the old dict to the new dict
            populations = new_populations

        return populations

    def save_data_genetic(self, schedule_index, time, cost) -> None:
        """
        This function saves the data made in genetic
        """
        self.data.append({'Schedule Index': schedule_index, 'Duration': time, 'Cost': cost})

    def export_data_genetic(self, experiment) -> None:
        """
        This function exports the data collected in genetic to a csv
        """

        # Set headers
        fields = ['Schedule Index', 'Duration', 'Cost']

        # Open the csv
        with open(f'data/experiment{experiment}.csv', 'a', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fields)

            # Only write the headers on first iterations
            if self.experiment_iter == 0:
                csv_writer.writeheader()

            # Add all data
            for row in self.data:
                csv_writer.writerow(row)

    """ Methods """

    def run_HC(self, hc_tuple):
        '''Method gets called to run and climb 1 Hillclimber, depending on the parameters inside the tuple'''
        
        # what hillclimber to run, current schedule, temperature, and number of iterations the hillclimber gets
        activation, schedule, T, hill_climber_iters = hc_tuple
        if activation == 0:

            # create the class and climb.
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(schedule, self.hillclimber_iter_counter)
            schedule, malus, iteration, accept_me = HC1.climb(hill_climber_iters, T=T, ANNEALING=self.ANNEALING, fail_counter=self.fail_counter)

            return schedule, malus, HC1.get_name(), iteration, accept_me

        elif activation == 1:

            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(schedule, self.hillclimber_iter_counter)
            schedule, malus, iteration, accept_me = HC2.climb(hill_climber_iters, T=T, ANNEALING=self.ANNEALING, fail_counter=self.fail_counter)

            return schedule, malus, HC2.get_name(), iteration, accept_me

        elif activation == 2:

            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(schedule, self.hillclimber_iter_counter)
            schedule, malus, iteration, accept_me = HC3.climb(hill_climber_iters, T=T, ANNEALING=self.ANNEALING, fail_counter=self.fail_counter)

            return schedule, malus, HC3.get_name(), iteration, accept_me

        elif activation == 3:

            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(schedule, self.hillclimber_iter_counter)
            schedule, malus, iteration, accept_me = HC4.climb(hill_climber_iters, T=T, ANNEALING=self.ANNEALING, fail_counter=self.fail_counter)

            return schedule, malus, HC4.get_name(), iteration, accept_me

    def __get_temperature(self, t, alpha=0.995):
        """Exponential decay temperature schedule"""
        return t * alpha

    def __replace_roster(self, difference):

        # print output
        if difference >= 0:
            print(f'\n========================= Generation: {self.multiprocessor_counter} =========================\n')
            print(f'Malus improvement: {difference}')
            print(f'Duration of iteration: {round(self.multiprocess_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)

        else:
            self.fail_counter += 1
            print(f'\n========================= Generation: {self.multiprocessor_counter} =========================\n')
            print('FAIL')
            print(f'Duration of iteration: {round(self.multiprocess_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)

    def recursive_copy(self, obj):
        '''
        method that makes a copy of our schedule that does not change the schedule
        when we modify the copy. This eliminates the need for deepcopy
        '''
        if isinstance(obj, dict):
            return {k: self.recursive_copy(v) for k, v in obj.items()}
        elif isinstance(obj, set):
            return {self.recursive_copy(x) for x in obj}
        else:
            return obj

    def save_schedule(self, schedule):
        """
        This function saves the input shedule using pickle
        """
        with open('schedule.pkl', 'wb') as f:
            pickle.dump(schedule, f)