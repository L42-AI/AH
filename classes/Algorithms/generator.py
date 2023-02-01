import classes.algorithms.optimize as OptimizeClass
import classes.representation.malus_calc as MalusCalculatorClass
import classes.representation.roster as RosterClass

from data.assign import course_list, student_list, room_list

import matplotlib.pyplot as plt
from tqdm import tqdm
import random
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
        self.malus, self.schedule = self.initialize(student_list, course_list, room_list)

        if visualize:
            self.plot_startup()

    """ INIT """

    def schedule_fill(self, student_list, course_list, room_list):
        """
        This method creates the schedule
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

        if self.DIFFICULT_STUDENTS:
            course_list = sorted(course_list, key=lambda x: x.prioritise)
            for i in range(5):
                course_list[i].lecture_day = days[i]

        for course in course_list:
            # go over the number of lectures and fill the schedule
            for i in range(course.lectures):

                self.fill_schedule_random(course, "lecture", i + 1, room_list)

            # make a dictionary to loop over with practicals and tutorials
            seminars = {
                'tutorial': (course.tutorials, course.tutorial_rooms),
                'practical': (course.practicals, course.practical_rooms)
            }

            # loop over the dict items for each seminar and their rooms needed
            for seminar_type, (num_seminars, num_rooms) in seminars.items():
                for i in range(num_seminars):
                    for j in range(num_rooms):
                        self.fill_schedule_random(course, seminar_type, j + 1, room_list)

        # timeslots in rooms that did not get used will be placed in the schedule as empty
        self.fill_empty_slots(room_list)

        self.init_student_timeslots(student_list)

    def init_student_timeslots(self, student_list):
        """This method takes in a student list and initializes student time slots for all the students."""

        # loop over the list of students and initialize timeslots
        for student in student_list:
            student.student_timeslots(self)

    def __place_in_schedule(self, room, day, timeslot, course_name, classes, max_std):
        """ This method places a dictionary into the right class with all the necessary information """

        # set all the necessary information into the dictionary for the right class key
        self.schedule[course_name][classes] = {}
        self.schedule[course_name][classes]['day'] = day
        self.schedule[course_name][classes]['timeslot'] = timeslot
        self.schedule[course_name][classes]['room'] = room.id
        self.schedule[course_name][classes]['capacity'] = room.capacity
        self.schedule[course_name][classes]['max students'] = max_std
        self.schedule[course_name][classes]['students'] = set()

        # set the room availability to False in order to negate double rostering of rooms
        room.availability[day][timeslot] = False

    def fill_empty_slots(self, room_list):
        """
        This method makes a new key in the schedule and as value fills all the rooms and their timeslots,
        that have not been scheduled yet.
        """

        # Set possible timeslots and days
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # add new key to the schedule
        self.schedule["No course"] = {}

        # count the empty seminar moments
        i = 0

        # check every room if they are being used at every moment
        for room in room_list:

            # Set timeslot lists
            timeslots = [9, 11, 13, 15]

            # if the room is C0.110 check the late timeslot as well
            if room.id == 'CO.110':
                timeslots = [9, 11, 13, 15, 17]

            for day in days:
                for timeslot in timeslots:
                    if room.availability[day][timeslot]:
                        classes = f"No classes {i}"

                        # schedule the room as empty
                        self.__place_in_schedule(room, day, timeslot, "No course", classes, 1000)

                        i += 1

    def fill_schedule_random(self, course, class_type, count, room_list):
        """ This function fills a schedule with no student capacity restraints in a random fassion """

        # Make key if not existent
        if course.name not in self.schedule:
            self.schedule[course.name] = {}

        # counter
        i = 0

        succes = False
        while not succes:

            # count plus 1
            i += 1

            # Generate a random room, day and timeslot:
            room = random.choice(room_list)
            day = random.choice(list(room.availability.keys()))
            timeslot = random.choice(list(room.availability[day].keys()))

            # If timeslot is available
            if room.availability[day][timeslot]:

                # first try with specific room for the type of class / part of the greedy algorithm
                if self.CAPACITY:
                    if i < 20:
                        if class_type == 'lecture' and room.id == 'A1.08' or room.id == 'A1.06':
                            continue
                        if class_type != 'lecture' and room.id == 'C0.110' or room.id == 'C0.112':
                            continue

                # check if the lecture_day is None if not check if its a lecture, if it is skip the rostering
                # part of the most POPULAR and DIFICULT_STUDENTS algorithm in generator.py
                if course.lecture_day != None:
                    if course.lecture_day != day and class_type == 'lecture':
                        continue

                self.schedule[course.name][f'{class_type} {count}'] = {}
                class_number = f"{class_type} {count}"

                # if the class is a tutorial roster it
                if class_number[0] == 't':
                    self.__place_in_schedule(room, day, timeslot, course.name, class_number, course.max_std_tutorial)\

                # if the class is a practical roster it
                elif class_number[0] == 'p':
                    self.__place_in_schedule(room, day, timeslot, course.name, class_number, course.max_std_practical)

                # roster the lecture
                else:
                    self.__place_in_schedule(room, day, timeslot, course.name, class_number, 1000)

                succes = True
            i += 1


    def initialize(self, student_list, course_list, room_list):

        self.schedule = {}

        # Fill the roster
        self.schedule_fill(student_list, course_list, room_list)

        # Compute Malus
        malus = self.MC.compute_total_malus(self.schedule)

        return malus, self.schedule

    """ METHODS """

    def __run_random(self):
        self.costs = []
        self.iterations = []
        for i in tqdm(range(100)):

            self.costs.append(self.initialize(student_list, course_list, room_list)[0]['Total'])

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

        Optimize = OptimizeClass.Optimize(self.schedule, self.ANNEALING, experiment_iter)

        if mode == 'sequential':
            Optimize.run_solo(algorithm_duration, experiment, core_assignment, hill_climber_iters)
        elif mode == 'multiproccesing':
            Optimize.run_multi(algorithm_duration, experiment, core_assignment, hill_climber_iters)
        elif mode == 'genetic':
            Optimize.run_genetic(algorithm_duration, experiment)
        elif mode == 'genetic pool':
            Optimize.run_genetic_pool(algorithm_duration, experiment, core_assignment, hill_climber_iters)