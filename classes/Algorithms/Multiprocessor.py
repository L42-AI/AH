import classes.algorithms.hillclimber as HillCLimberClass
from multiprocessing import Pool
import random



import pandas as pd
import time
import json
import copy
import matplotlib.pyplot as plt

class Multiprocessor():
    '''Multiprocessor class calls on hillclimbers in a specific order. That order can distribute
       the hillclimbers based on malus or spread it out evenly. It handles the pooling of the hillclimbers, 
       making the proces much faster. Starting up the pools takes time, but when we run multiple hillclimber
       iterations per call, it makes up for it.'''

    def __init__(self, Roster, course_list, student_list, MC, annealing=False, multiplier=0.1):
        self.Roster = Roster
        self.course_list = course_list
        self.student_list = student_list
        self.ITERS = 1000
        self.ANNEALING = annealing
        self.multiplier = multiplier

        self.MC = MC

    def core_assignment(self, malus) -> list:
        '''creates a lists with integers representing hillclimber classes based on
           the current malus proportions, so when there are more gap hours, more students
           will be switched and when there are more capacity malus points, more lectures and tutorials 
           etc will be switched'''

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

    def run(self):
        '''Handles the process of running and stores that data for the GUI. This is
           the main proces for finding the schedule'''
        # Set lists for several runs
        self.list_iterations = []
        self.list_total_malus = []
        self.list_class_random = []
        self.list_class_capacity = []
        self.list_student_gaphour = []
        self.list_student_doublehour = []
        self.list_duration_since_innit = []

        # # set lists for one run with all the different hillclimber steps
        # hillclimber_class_random_iterations = []
        # hillclimber_class_random_malus = []

        # hillclimber_class_capacity_iterations = []
        # hillclimber_class_capacity_malus = []
        
        # hillclimber_student_gaphour_iterations = []
        # hillclimber_student_gaphour_malus = []

        # hillclimber_student_doublehour_iterations = []
        # hillclimber_student_doublehour_malus = []

        self.info = {}

        # Set counters
        self.iter_counter = 0
        self.fail_counter = 0

        # Set Initial variable
        self.duration = 0

        self.schedule = self.Roster.schedule

        self.malus = self.MC.compute_total_malus(self.schedule)

        # append initialized malus and 0 for the differences
        self.list_total_malus.append(self.malus['Total'])
        self.list_class_random.append(0)
        self.list_class_capacity.append(0)
        self.list_student_gaphour.append(0)
        self.list_student_doublehour.append(0)
        self.list_iterations.append(0)
        self.list_duration_since_innit.append(0)

        core_assignment_list = [0,1,2,3]

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)
        if self.ANNEALING:
            t = .8
        else:
            t = 0
        # while self.Roster.malus_cause['Dubble Classes'] != 0 or self.Roster.malus_cause['Capacity'] != 0:
        while self.fail_counter < 30:
        # while self.iter_counter != 2:

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

            start_time = time.time()

            # Make four deepcopys for each function to use
            self.schedules = [copy.copy(self.schedule) for _ in range(4)]

                
            self.malus = self.MC.compute_total_malus(self.schedule)
            # Fill the pool with all functions and their rosters
            with Pool(4) as p:
                self.output_schedules = p.map(self.run_HC, [(core_assignment_list[0], self.schedule, t, self.malus['Total']),
                                                            (core_assignment_list[1], self.schedule, t, self.malus['Total']),
                                                            (core_assignment_list[2], self.schedule, t, self.malus['Total']),
                                                            (core_assignment_list[3], self.schedule, t, self.malus['Total'])])
            for _, accept_now in enumerate(self.output_schedules[5]):
                if accept_now:
                    self.best_index = _
                    self.__replace_roster(difference, accept=True)
                    continue

            # find the lowest malus of the output rosters
            min_malus = min([i[1]['Total'] for i in self.output_schedules])

            # Use the lowest malus to find the index of the best roster
            self.best_index = [i[1]['Total'] for i in self.output_schedules].index(min_malus)

            # Compute difference between new roster and current roster
            difference = self.malus['Total'] - self.output_schedules[self.best_index][1]['Total']

            # append the difference each hillclimber made
            self.list_class_random.append(self.malus['Total'] - self.output_schedules[0][1]['Total'])
            self.list_class_capacity.append(self.malus['Total'] - self.output_schedules[1][1]['Total'])
            self.list_student_gaphour.append(self.malus['Total'] - self.output_schedules[2][1]['Total'])
            self.list_student_doublehour.append(self.malus['Total'] - self.output_schedules[3][1]['Total'])


            # # append the different hillclimbers malus and iterations
            # hillclimber_class_random_iterations.extend([x + (self.iter_counter * 50) for x in self.output_schedules[0][3]])
            # hillclimber_class_random_malus.extend(self.output_schedules[0][4])

            # hillclimber_class_capacity_iterations.extend([x + (self.iter_counter * 50) for x in self.output_schedules[1][3]])
            # hillclimber_class_capacity_malus.extend(self.output_schedules[1][4])

            # hillclimber_student_gaphour_iterations.extend([x + (self.iter_counter * 50) for x in self.output_schedules[2][3]])
            # hillclimber_student_gaphour_malus.extend(self.output_schedules[2][4])

            # hillclimber_student_doublehour_iterations.extend([x + (self.iter_counter * 50) for x in self.output_schedules[3][3]])
            # hillclimber_student_doublehour_malus.extend(self.output_schedules[3][4])

            # Set finish time
            finish_time = time.time()

            self.iter_duration = finish_time - start_time
            self.duration += self.iter_duration

            # replace the roster if it is better
            self.__replace_roster(difference)

            # Increase iter counter
            self.iter_counter += 1
            
            # append iteration and duration
            self.list_iterations.append(self.iter_counter)
            self.list_duration_since_innit.append(round(self.duration, 2))

            # append the total malus
            self.list_total_malus.append(self.malus['Total'])

        # # do this only for the one from luka
        # data = {
        #     'Iterations': hillclimber_class_random_iterations,
        #     'Malus Class Random': hillclimber_class_random_malus,
        #     # 'Iterations Class Capacity': hillclimber_class_capacity_iterations,
        #     'Malus Class Capacity': hillclimber_class_capacity_malus,
        #     # 'Iterations Student Gaphour': hillclimber_student_gaphour_iterations,
        #     'Malus Student Gaphour': hillclimber_student_gaphour_malus,
        #     # 'Iterations Student Doublehour': hillclimber_student_doublehour_iterations,
        #     'Malus Student Doublehour': hillclimber_student_doublehour_malus
        # }
    
        # df = pd.DataFrame(data)

        # df.to_csv('data/Lukas Plot Data.csv')
        # print(df)

        return self.list_iterations, self.list_total_malus, self.list_class_random, self.list_class_capacity, self.list_student_gaphour, self.list_student_doublehour, self.list_duration_since_innit

    def run_HC(self, hc_tuple):
        '''method that run calls on with a list that is used to determine what hillclimbers should run.
           The hillclimbers can be activated seperate from each other. Each hillclimber returns a schedule, 
           malus and the name of the hillclimber that was used'''
        activation, schedule, T, real_score = hc_tuple
        if activation == 0:
            # print('looking to swap classes...')
            HC1 = HillCLimberClass.HC_TimeSlotSwapRandom(schedule, self.course_list, self.student_list, self.MC, self.multiplier)

            schedule, malus, list_iterations, list_malus, accept_me = HC1.climb(T, self.fail_counter)
        
            # print(f'HC1: {roster.malus_count}')
            return schedule, malus, HC1.get_name(), list_iterations, list_malus, accept_me

        elif activation == 1:
            # print('looking to swap students randomly...')
            HC2 = HillCLimberClass.HC_TimeSlotSwapCapacity(schedule, self.course_list, self.student_list, self.MC, self.multiplier)

            
            schedule, malus, list_iterations, list_malus, accept_me = HC2.climb(T, self.fail_counter)
            # print(f'HC2: {roster.malus_count}')
            return schedule, malus, HC2.get_name(), list_iterations, list_malus, accept_me

        elif activation == 2:
            # print('looking to swap students on gap hour malus...')
            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(schedule, self.course_list, self.student_list, self.MC, self.multiplier)
            schedule, malus, list_iterations, list_malus, accept_me = HC3.climb(T, self.fail_counter)
            # print(f'HC3: {roster.malus_count}')
            return schedule, malus, HC3.get_name(), list_iterations, list_malus, accept_me

        elif activation == 3:
            # print('looking to swap students on double classes malus...')
            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(schedule, self.course_list, self.student_list, self.MC, self.multiplier)
            schedule, malus, list_iterations, list_malus, accept_me = HC4.climb(T, self.fail_counter)
            # print(f'HC4: {roster.malus_count}')
            return schedule, malus, HC4.get_name(), list_iterations, list_malus, accept_me

    def __get_temperature(self, t, alpha=0.995):
        """Exponential decay temperature schedule"""
        return t*alpha

    def __replace_roster(self, difference, accept=False):
        '''replaces the current schedule with a new one if the malus is lower'''

        if accept:
            self.schedule, self.malus, name, iterations, malus, _ = self.output_schedules[self.best_index]
            self.fail_counter = 0

            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print(f'Accepted worsening from: {name}')
            print(f'Malus worsening: {-difference}')
            print(f'Duration of iteration: {round(self.iter_duration, 2)} S.')
            print(f'Duration since init: {round(self.duration, 2)} S.')
            print(self.malus)
            return
        # If difference is positive
        if difference > 0:

            # Set the new roster to self.Roster
            self.schedule, self.malus, name, iterations, malus, _ = self.output_schedules[self.best_index]
            self.fail_counter = 0

            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print(f'Most effective function: HC{name}')
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
            self.schedule, self.malus, name = self.output_schedules[self.best_index]
            print(self.best_index)
            self.fail_counter = 0

            print(f'\n========================= Generation: {self.iter_counter} =========================\n')
            print(f'Most effective function: HC{name}')
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

class Multiprocessor_SimAnnealing(Multiprocessor):

    def __replace_roster(self, difference):
        # set the temperature
        T = (150/(200 + self.iter_counter*2))

        # If difference is positive
        if difference > 0:

            # Set the new roster to self.Roster
            self.schedule, self.malus, _ = self.output_schedules[self.best_index]
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