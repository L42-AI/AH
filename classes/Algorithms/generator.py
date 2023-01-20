import classes.Algorithms.mutate as MutateClass
import classes.Algorithms.hillclimber as HillCLimberClass
import classes.representation.course as CourseClass
import classes.representation.student as StudentClass
import classes.representation.room as RoomClass
import classes.representation.roster as RosterClass
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
import time
import random

from tqdm import tqdm

class Generator():
    def __init__(self, COURSES, STUDENT_COURSES, ROOMS, visualize=False):

        self.malus, self.Roster, self.df, self.course_list, self.student_list, self.rooms_list = self.initialise(COURSES, STUDENT_COURSES, ROOMS)

        if visualize:
            self.plot_startup(COURSES, STUDENT_COURSES, ROOMS)

    def __count_students(self, df):
        """This function Counts the amount of students enrolled for each course"""

        list_courses = ['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']
        dict_count = {}

        # loop over each row of the dataframe and set the count plus 1
        for _, row in df.iterrows():
            for course in list_courses:

                # make it a string, in order to easily check if it is nan
                course_str = str(row[course])

                if course_str != 'nan':

                    # check if its in the dict, if not make a key and set value to 0
                    if course_str not in dict_count:
                        dict_count[course_str] = 0

                    # count the students
                    dict_count[course_str] += 1

        return dict_count

    def assign(self, COURSES, STUDENT_COURSES, ROOMS):
        """This Function takes in 3 Dataframes, loops over the dataframe and fills a list with the respective Class objects."""

        course_list = []
        student_list = []
        rooms_list = []

        # count the students that have enrolled for each course
        dict_enrollment = self.__count_students(STUDENT_COURSES)

        # create an instance for every course
        for _, course in COURSES.iterrows():

            # fill in the list with course objects
            course_list.append(CourseClass.Course(course, dict_enrollment[course['Vak']]))

        for _, student in STUDENT_COURSES.iterrows():

            # fill in the list with student objects
            student_list.append(StudentClass.Student(student, course_list))

        for _, room in ROOMS.iterrows():

            # fill in the list with room objects
            rooms_list.append(RoomClass.Room(room))

        for course in course_list:
            course.enroll_students(student_list)

        return course_list, student_list, rooms_list


    def schedule_fill(self, Roster, course_list, student_list):
        ''''method schedules a timeslot for every lecture, tutorial or practical that takes place'''

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

        Roster.init_student_timeslots(student_list)


    def create_dataframe(self, Roster, student_list, visualize=False):
        # Make lists to put into schedule dataframe
        df_list_student_object = []
        df_list_student_malus = []
        df_list_students = []
        df_list_courses = []
        df_list_type = []
        df_list_rooms = []
        df_list_day = []
        df_list_time = []

        # For each student:
        for student in student_list:

            # For each course:
            for course_timeslot in student.timeslots:

                # For each class:
                for class_timeslot in student.timeslots[course_timeslot]:

                    # Set timeslot
                    timeslot = student.timeslots[course_timeslot][class_timeslot]

                    # Add all relevant information ito lists
                    df_list_student_object.append(student)
                    df_list_student_malus.append(student.malus_count)
                    df_list_students.append(f'{student.f_name} {student.l_name}')
                    df_list_courses.append(course_timeslot)
                    df_list_type.append(class_timeslot)
                    df_list_rooms.append(timeslot['room'])
                    df_list_day.append(timeslot['day'])
                    df_list_time.append(timeslot['timeslot'])


        # Create schedule
        schedule_df = pd.DataFrame({'Student Object': df_list_student_object,
                                    'Student Name': df_list_students,
                                    'Course': df_list_courses,
                                    'Activity': df_list_type,
                                    'Room': df_list_rooms,
                                    'Day': df_list_day,
                                    'Time': df_list_time,
                                    'Student Malus': df_list_student_malus,
                                    'Total Malus': Roster.malus_count})

        if visualize:
            # Current working directory
            current_dir = os.getcwd()

            # Parent directory
            parent_dir = os.path.dirname(current_dir)

            # Directory "visualize"
            visualize_directory = os.path.join(parent_dir, 'AH/visualize')

            # Export to excel file
            schedule_df.to_excel(f"{visualize_directory}/schedule.xlsx", index=False)

        return schedule_df


    def initialise(self, COURSES, STUDENT_COURSES, ROOMS):
        # starts up a random Roster

        course_list, student_list, rooms_list = self.assign(COURSES, STUDENT_COURSES, ROOMS)

        # create a roster
        Roster = RosterClass.Roster(rooms_list, student_list, course_list)

        # fill the roster
        self.schedule_fill(Roster, course_list, student_list)

        # Calculate costs of roster
        Roster.total_malus(student_list)

        # Create a dataframe and export to excel for visual representation
        df = self.create_dataframe(Roster, student_list)

        # Save as malus points
        malus_points = Roster.malus_count

        return malus_points, Roster, df, course_list, student_list, rooms_list


    def __run_random(self, COURSES, STUDENT_COURSES, ROOMS):
        self.costs = []
        self.iterations = []
        for i in tqdm(range(300)):

            self.costs.append(self.initialise(COURSES, STUDENT_COURSES, ROOMS)[0])

            self.iterations.append(i)

    def plot_startup(self, COURSES, STUDENT_COURSES, ROOMS):
        '''plots 300 random startups to get an idea of what a random score would be'''

        self.__run_random(COURSES, STUDENT_COURSES, ROOMS)

        fig_name = "startups.png"

        # Current working directory
        current_dir = os.getcwd()

        # Parent directory
        parent_dir = os.path.dirname(current_dir)

        # Directory "visualize"
        directory_plots = os.path.join(parent_dir, 'AH/visualize')

        # Fit a polynomial of degree 1 (i.e. a linear regression) to the data
        coefficients = np.polyfit(self.iterations, self.costs, 1)

        # Create a new set of x values for the regression line
        x_reg = np.linspace(min(self.iterations), max(self.iterations), 300)

        # Use the coefficients to calculate the y values for the regression line
        y_reg = np.polyval(coefficients, x_reg)

        plt.title('300 random startups of the algorithm with no restrictions')
        plt.plot(self.iterations, self.costs)

        # Plot the regression line
        plt.plot(x_reg, y_reg, 'r')
        plt.xlabel('run #')
        plt.ylabel('malus points')
        plt.savefig(os.path.join(directory_plots, fig_name))
        plt.show()

    def get_schedule(self):
        return self.Roster.schedule

    def get_malus(self):
        return self.Roster.malus_count

    def get_malus_cause(self):
        return self.Roster.all_malus_cause

    def run(self, iters = 200):
        for i in tqdm(range(iters)):
            self.costs.append()
            self.iterations.append(i)

    def rearrange(self):

        start = time.time()
        start_cost = self.Roster.malus_count
        for i in range(10):
            for _ in range(5):
                i = random.randint(0,5)
                if i == 0:
                    HC1 = HillCLimberClass.HC_StudentSwap(self.Roster, self.df, self.course_list, self.student_list)
                    self.Roster = HC1.climb()

                elif i == 1:
                    HC2 = HillCLimberClass.HC_StudentSwapRandom(self.Roster, self.df, self.course_list, self.student_list)
                    self.Roster = HC2.climb()

                elif i == 2:
                    HC3 = HillCLimberClass.HC_StudentSwitch(self.Roster, self.df, self.course_list, self.student_list)
                    self.Roster = HC3.climb()

                elif i == 3:
                    HC4 = HillCLimberClass.HC_LectureLocate(self.Roster, self.df, self.course_list, self.student_list)
                    self.Roster = HC4.climb()

                else:
                    HC5 = HillCLimberClass.HC_LectureSwap(self.Roster, self.df, self.course_list, self.student_list)
                    self.Roster = HC5.climb()

        finish = time.time()
        final_cost = self.Roster.malus_count
        print('100 iters')
        print(f'start: {start_cost}')
        print(f'finish: {final_cost}')
        print(f'Time taken: {finish - start}')




