import classes.algorithms.multiprocessor as MultiprocessorClass
import classes.representation.malus_calc as MalusCalculatorClass
import classes.representation.roster as RosterClass

from data.assign import course_list

import matplotlib.pyplot as plt
from tqdm import tqdm
import os

class Generator:
    def __init__(self, capacity, popular, popular_own_day, difficult_students, annealing, visualize):

        # Set heuristics
        self.CAPACITY = capacity
        self.POPULAR = popular
        self.POPULAR_OWN_DAY = popular_own_day
        self.ANNEALING = annealing
        self.DIFFICULT_STUDENTS = difficult_students
        self.MC = MalusCalculatorClass.MC()

        # Save initialization
        self.malus, self.Roster = self.initialise()

        if visualize:
            self.plot_startup()

    """ INIT """

    def schedule_fill(self, Roster, course_list):
        ''''method schedules a timeslot for every lecture, tutorial or practical that takes place'''

        # first give the most popular courses a place in the schedule
        if self.POPULAR:
            course_list = sorted(course_list, key = lambda x: x.enrolled, reverse = True)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        # give the 5 most popular courses their own day to hold their lectures, to prevent gap hours
        if self.POPULAR_OWN_DAY:

            for i in range(5):
                course_list[i].day = days[i]

        if self.DIFFICULT_STUDENTS:
            course_list = sorted(course_list, key=lambda x: x.prioritise)
            for i in range(5):
                course_list[i].day = days[i]

        for course in course_list:
            # go over the number of lectures, tutorials and practicals needed
            for i in range(course.lectures):
                # check how many students will attend this lecture
                attending = course.enrolled
                Roster.fill_schedule_random(course, "lecture", i + 1, attending)

            # outer loop is incase more than one tut per group
            ## in csv there is always one tut or pract, but we want to make the program scalable 
            for _ in range(course.tutorials):
                for i in range(course.tutorial_rooms):

                    # check how many students will attend this tutorial
                    attending = course.tut_group_dict[i + 1]
                    Roster.fill_schedule_random(course, "tutorial", i + 1, attending)

            for _ in range(course.practicals):
                for i in range(course.practical_rooms):

                    # check how many students will attend this practical
                    attending = course.pract_group_dict[i + 1]
                    Roster.fill_schedule_random(course, "practical", i + 1, attending)

        # timeslots in rooms that did not get used will be placed in the schedule as empty
        Roster.fill_empty_slots()

        Roster.init_student_timeslots()

    def initialise(self):

        # Create a roster
        Roster = RosterClass.Roster(capacity=self.CAPACITY)

        # Fill the roster
        self.schedule_fill(Roster, course_list)

        # Compute Malus
        malus = self.MC.compute_total_malus(Roster.schedule)

        return malus, Roster

    """ GET """

    def get_schedule(self):
        return self.Roster.schedule

    """ METHODS """

    def __run_random(self):
        self.costs = []
        self.iterations = []
        for i in tqdm(range(100)):

            self.costs.append(self.initialise()[0]['Total'])

            self.iterations.append(i)

    def plot_startup(self):
        '''plots 300 random startups to get an idea of what a random score would be'''

        self.__run_random()

        if self.CAPACITY or self.POPULAR or self.POPULAR_OWN_DAY:
            fig_name = f'Baseline_Capacity:{self.CAPACITY}_Popular:{self.POPULAR}_Popular_own_day:{self.POPULAR_OWN_DAY}.png'
        else:
            fig_name = "Baseline_random.png"

        # Current working directory
        current_dir = os.getcwd()

        # Parent directory
        parent_dir = os.path.dirname(current_dir)

        # Directory "visualize"
        directory_plots = os.path.join(parent_dir, 'AH/visualize')

        plt.figure(figsize=(10,4))
        plt.style.use('seaborn-whitegrid')

        plt.title('Schedule Initialization (N = 500)')
        plt.hist(self.costs, bins=20, facecolor='#2ab0ff', edgecolor='#169acf', linewidth=0.5)

        # Plot the regression line
        plt.ylabel('Iterations')
        plt.xlabel('Malus')
        plt.savefig(os.path.join(directory_plots, fig_name))

    def optimize(self, experiment, mode, core_assignment, hill_climber_iters, algorithm_duration, experiment_iter=0):

        Multiprocessor = MultiprocessorClass.Multiprocessor(self.Roster, self.ANNEALING, experiment_iter)

        if mode == 'sequential':
            pass
        elif mode == 'multiproccesing':
            Multiprocessor.run_multi(algorithm_duration, experiment, core_assignment, hill_climber_iters)
        elif mode == 'genetic':
            Multiprocessor.run_genetic(algorithm_duration, experiment)
        elif mode == 'genetic pool':
            Multiprocessor.run_genetic_pool(algorithm_duration, experiment, core_assignment, hill_climber_iters)