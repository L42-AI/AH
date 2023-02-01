"""
This file includes the generator class which is the class that generates our schedule
It does the random initialization and can route the schedule to the optimizing class
"""

import classes.algorithms.optimize as OptimizeClass
import classes.representation.malus_calc as MalusCalculatorClass
import classes.representation.roster as RosterClass

from data.assign import course_list, room_list

import matplotlib.pyplot as plt
from tqdm import tqdm
import os

class Generator:
    """ This Class runs the optimize functions, randomly initiates the schedule and plots the baseline """

    def __init__(self, capacity, popular, popular_own_day, difficult_students, annealing, visualize):
        # Set heuristics
        self.CAPACITY = capacity
        self.POPULAR = popular
        self.POPULAR_OWN_DAY = popular_own_day
        self.ANNEALING = annealing
        self.DIFFICULT_STUDENTS = difficult_students
        self.MC = MalusCalculatorClass.MC()

        # Save initialization
        self.malus, self.Roster = self.initialize()

        # if in the GUI visualize is set to true show the graph of the baseline
        if visualize:
            self.plot_startup()

    def schedule_fill(self, Roster, course_list, room_list):
        """
        This method takes in a Roster Object, a list of Course Objects and a list of Roob Objects.
        It then fills the schedule of the Roster with the help of the course and room objects in a random fassion.
        """

        # Set the days list
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # Check heuristics state
        if self.POPULAR:
            # Sort the course list on popularity (enrolled)
            course_list = sorted(course_list, key = lambda x: x.enrolled, reverse = True)

        # give the 5 most popular courses their own day to hold their lectures, to prevent gap hours
        if self.POPULAR_OWN_DAY:
            for i in range(5):
                course_list[i].lecture_day = days[i]

        # give the 5 most 
        if self.DIFFICULT_STUDENTS:
            course_list = sorted(course_list, key=lambda x: x.prioritise)
            for i in range(5):
                course_list[i].lecture_day = days[i]

        # loop over the course list
        for course in course_list:

            # go over the number of lectures and fill the schedule
            for i in range(course.lectures):

                Roster.fill_schedule_random(course, "lecture", i + 1)

            # make a dictionary to loop over with practicals and tutorials
            seminars = {
                'tutorial': (course.tutorials, course.tutorial_rooms),
                'practical': (course.practicals, course.practical_rooms)
            }

            # loop over the dict items for each seminar and their rooms needed
            for seminar_type, (num_seminars, num_rooms) in seminars.items():
                for i in range(num_seminars):
                    for j in range(num_rooms):
                        Roster.fill_schedule_random(course, seminar_type, j + 1)

        # place unused timeslots in rooms in schedule as empty
        Roster.fill_empty_slots()

        # schedule in all students
        Roster.schedule_students()

        # reset all availability of rooms for in the case of doing several initiates
        Roster.reset_room_availability(room_list)

    def initialize(self):
        """
        This method initializes the roster
        """

        # Create a roster
        Roster = RosterClass.Roster(capacity=self.CAPACITY)

        # Fill the roster
        self.schedule_fill(Roster, course_list, room_list)

        # Compute Malus
        malus = self.MC.compute_total_malus(Roster.schedule)

        return malus, Roster

    def __run_random(self):
        """
        This method runs the initialize for 500 iterations and appends the malus points to the list cost
        """

        # make the lists
        self.costs = []
        self.iterations = []

        # Run the initialize function 500 times
        for i in tqdm(range(500)):

            self.costs.append(self.initialize()[0]['Total'])

            self.iterations.append(i)

    def plot_startup(self):
        """
        This method plots 500 random startups to get an idea of what a random score would be
        """

        # Run the random function
        self.__run_random()

        # Set the file name based on the heuristic that are enabled
        if self.CAPACITY or self.POPULAR or self.POPULAR_OWN_DAY:
            fig_name = f'Baseline_Capacity:{self.CAPACITY}_Popular:{self.POPULAR}_Popular_own_day:{self.POPULAR_OWN_DAY}_Busy_Students:{self.DIFFICULT_STUDENTS}.png'
        else:
            fig_name = "Baseline_random.png"

        # Current working directory
        current_dir = os.getcwd()

        # Parent directory
        parent_dir = os.path.dirname(current_dir)

        # Directory "visualize"
        directory_plots = os.path.join(parent_dir, 'AH/visualize')

        # Set settings for plot
        plt.figure(figsize=(10,4))
        plt.style.use('seaborn-whitegrid')

        plt.title('Schedule Initialization (N = 500)')
        plt.hist(self.costs, bins=20, facecolor='#2ab0ff', edgecolor='#169acf', linewidth=0.5)

        # Plot the regression line
        plt.ylabel('Iterations')
        plt.xlabel('Malus')
        plt.savefig(os.path.join(directory_plots, fig_name))
        plt.show()

    def optimize(self, experiment, mode, core_assignment, hill_climber_iters, algorithm_duration, experiment_iter=0):

        # initiate the optimze class
        Optimize = OptimizeClass.Optimize(self.Roster, self.ANNEALING, experiment_iter)

        # choose the right method from the optimize class to run
        if mode == 'sequential':
            Optimize.run_solo(algorithm_duration, experiment, core_assignment, hill_climber_iters)

        elif mode == 'multiproccesing':
            Optimize.run_multi(algorithm_duration, experiment, core_assignment, hill_climber_iters)

        elif mode == 'genetic':
            Optimize.run_genetic(algorithm_duration, experiment)

        elif mode == 'genetic pool':
            Optimize.run_genetic_pool(algorithm_duration, experiment, core_assignment, hill_climber_iters)