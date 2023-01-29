# dit is van main

if __name__ == '__main__':
    list_total_malus = []
    list_class_random = []
    list_class_capacity = []
    list_student_gaphour = []
    list_student_doublehour = []

    lists_to_append = [list_total_malus, list_class_random, list_class_capacity, list_student_gaphour, list_student_doublehour]

    # run the experiment 30 times
    for i in range(2):
        lists = main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT)

        for lst, list_to_append in zip(lists, lists_to_append):
            for value in lst:
                list_to_append.append(value)

    data = {
        'Total Malus': list_total_malus,
        'Swap Class Random': list_class_random, 
        'Swap Class Capacity': list_class_capacity,
        'Swap Student Gaphour': list_student_gaphour,
        'Swap Student Doublehour': list_student_doublehour
        }

    df = pd.DataFrame(data)

    print(df)

    df.to_csv('data/Normal Hillclimber.csv')

# vergeet niet return in main runner en generator en multiprocessor

# dit is van multiprocessor
def run(self):

        # Set lists
        self.list_total_malus = []
        self.list_class_random = []
        self.list_class_capacity = []
        self.list_student_gaphour = []
        self.list_student_doublehour = []

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

        core_assignment_list = [0,1,2,3]

        # Print intitial
        print(f'\nInitialization')
        print(self.malus)
        if self.ANNEALING:
            t = 1
        else:
            t = 0
        # while self.Roster.malus_cause['Dubble Classes'] != 0 or self.Roster.malus_cause['Capacity'] != 0:
        # while self.fail_counter <= 30:
        while self.iter_counter != 2:

            start_time = time.time()

            if self.ANNEALING:
                t = self.__get_temperature(t)
                if t < 0.01:
                    t = 0.05
            else:
                t = 0

            start_time = time.time()

            # Make four deepcopys for each function to use
            self.schedules = [copy.copy(self.schedule) for _ in range(4)]

            if self.malus['Capacity'] < 10:
                core_assignment_list = [0,1,2,3]
                
            self.malus = self.MC.compute_total_malus(self.schedule)
            # Fill the pool with all functions and their rosters
            with Pool(4) as p:
                self.output_schedules = p.map(self.run_HC, [(core_assignment_list[0], self.schedule, t, self.malus['Total']),
                                                            (core_assignment_list[1], self.schedule, t, self.malus['Total']),
                                                            (core_assignment_list[2], self.schedule, t, self.malus['Total']),
                                                            (core_assignment_list[3], self.schedule, t, self.malus['Total'])])

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

            # Set finish time
            finish_time = time.time()

            self.iter_duration = finish_time - start_time
            self.duration += self.iter_duration


            # replace the roster if it is better
            self.__replace_roster(difference)

            # Increase iter counter
            self.iter_counter += 1

            
            # append the total malus
            self.list_total_malus.append(self.malus['Total'])
    
        return self.list_total_malus, self.list_class_random, self.list_class_capacity, self.list_student_gaphour, self.list_student_doublehour

