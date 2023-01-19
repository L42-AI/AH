"""
This file includes the class Student which represents each student.
The data used comes from the given dataframe.
add_courses and select_groups are part of the initialisation.
student_timeslot, malus_point are two methods to compute the malus points.
compute_malus runs these functions.
"""

import random

class Student():
    def __init__(self, data, courses):

        # Set attributes
        self.f_name = data['Voornaam']
        self.l_name = data['Achternaam']
        self.id = data['Stud.Nr.']

        # Import the name of the course from the data
        self.courses_names = [course for course in data[3:] if str(course) != 'nan']

        # Create the list of which course objects
        self.init_courses(courses)

        # Make dictionaries for practicum and tutorial groups
        self.select_groups()

        # Make list of timeslots
        self.timeslots = {}

        # Initiate malus
        self.init_malus()

    # def __str__(self):
    #     return f"{self.f_name} {self.l_name}"

    def init_malus(self):
        self.malus_count = 0
        self.malus_cause = {}
        self.malus_cause['Classes Gap'] = 0
        self.malus_cause['Dubble Classes'] = 0

    def init_courses(self, courses):
        """ Assign all the courses to the student and set the enrollment dictionary """

        self.courses = []

        # For each course:
        for name in self.courses_names:

            # Add courses to the courses list
            for course in courses:
                if course.name == name:
                    self.courses.append(course)


    def __set_type(self, course, class_type):
        """ This function sets parameters used in pick_group"""

        # If class is tutorial:
        if class_type == 'Tutorial':

            # Set all values of tutorial
            group_dict = course.tut_group_dict
            class_num = course.tutorials
            max_std = course.max_std
            group = self.tut_group
        else:
            # Set all values of practica
            group_dict = course.pract_group_dict
            class_num = course.practica
            max_std = course.max_std_practica
            group = self.pract_group

        return group_dict, class_num, max_std, group

    def __pick_group(self, course, group_dict, class_num, max_std, group):
        """ This function picks a group based on the given arguments """

        # Only run if there are 1 or more classes
        if class_num >= 1:

            # Set completed boolean
            group_picked = None

            # Set amount of possible groups
            possible_groups = list(group_dict)[-1]

            # While no group is picked
            while not group_picked:

                # Generate a random group
                group_picked = random.randint(1, possible_groups)

                # If group is not full (smaller than max_std)
                if group_dict[group_picked] < max_std:

                    # Add group count
                    group_dict[group_picked] += 1

                    # Set the picked group as student attribute
                    group[course.name] = group_picked
                else:
                    # Reset group picked to remain in loop
                    group_picked = None

    def select_groups(self):
        """ This function selects groups of tutorial and practica for each course """

        self.tut_group = {}
        self.pract_group = {}

        # For each course
        for course in self.courses:

            # For each of the class types (with groups):
            for class_type in ['Tutorial', 'Practica']:

                # Set the variable of the correct class
                group_dict, class_num, max_std, group = self.__set_type(course, class_type)

                # Run the pick group function
                self.__pick_group(course, group_dict, class_num, max_std, group)


    def __lecture_timeslot(self, course, current_course):

        if course.lectures > 0:
            # For each lecture in the course:
            for index in range(course.lectures):

                # Set the current class
                current_lecture = f"lecture {index + 1}"

                # Add course and class to timeslot info
                timeslot_dict = current_course[current_lecture]

                self.timeslots[course.name][current_lecture] = timeslot_dict

    def __tutorial_timeslot(self, course, current_course):

        if course.tutorials > 0:
            # For each tutorial in the course:
            for index in range(course.tutorials):

                # Set the current class
                # tut*index is incase group needs 2 tutorials, so they need timeslots from 2 entries
                current_tutorial = f"tutorial {(self.tut_group[course.name] + self.tut_group[course.name] * index)}"

                # Add course and class to timeslot info
                timeslot_dict = current_course[current_tutorial]

                self.timeslots[course.name][current_tutorial] = timeslot_dict

    def __practicum_timeslot(self, course, current_course):

        if course.practica > 0:
            # For each practicum in the course:
            for index in range(course.practica):

                # Set the current class
                # tut*index is incase group needs 2 tutorials, so they need timeslots from 2 entries
                current_practicum = f"practical {(self.pract_group[course.name] + self.pract_group[course.name] * index)}"

                # Add course and class to timeslot info
                timeslot_dict = current_course[current_practicum]

                self.timeslots[course.name][current_practicum] = timeslot_dict

    def student_timeslots(self, Roster):
        """ 
        This method adds the timeslots for classes per week. 
        The dictionary timeslots is linked to the Roster schedule.
        """

        # For each course:
        for course in self.courses:

            self.timeslots[course.name] = {}

            # Set the current course dict
            current_course = Roster.schedule[course.name]

            # Find and save the lecture timeslot
            self.__lecture_timeslot(course, current_course)

            # Find and save the tutorial timeslot
            self.__tutorial_timeslot(course, current_course)

            # Find and save the practicum timeslot
            self.__practicum_timeslot(course, current_course)


    def __days_in_schedule(self):

        # Create a days dictionary
        days = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}

        # For each timeslot:
        for timeslot_course in self.timeslots:
            for timeslot_class in self.timeslots[timeslot_course]:

                timeslot = self.timeslots[timeslot_course][timeslot_class]

                # Add the timeslots into the days dictionary
                days[timeslot['day']].append(timeslot['timeslot'])
        return days

    def malus_points(self):
        """ This method calculates the malus points point for the student """
        # Reset malus points to avoid summing dubble malus
        self.init_malus()

        # find how often student has classes per day
        days = self.__days_in_schedule()

        # go over the days
        for day in days:

            # Sort the timeslots in the day:
            days[day].sort(reverse=True)

            # Set the dictionary key as list
            timeslot_list = days[day]

            # Only compute if list includes more than 1 timeslot
            if len(timeslot_list) > 1:

                # keep track if students have double classes that day
                timeslots_double_classes = []

                # For each timeslot number: (range is -1 to ensure the use of index + 1)
                for timeslot_num in range(len(timeslot_list) - 1):

                    # malus for double classes
                    if timeslot_list[timeslot_num] in timeslots_double_classes:
                        self.malus_cause['Dubble Classes'] += 1
                        self.malus_count += 1
                    else:
                        timeslots_double_classes.append(timeslot_list[timeslot_num])

                    # some cases, double booking might be allowed, but we do not want to add 2 malus
                    if timeslot_list[timeslot_num] - timeslot_list[timeslot_num + 1] != 0:
                        malus = int((timeslot_list[timeslot_num] - (timeslot_list[timeslot_num + 1] + 2)) / 2)
                        self.malus_cause['Classes Gap'] += malus
                        self.malus_count += malus

                    else:
                        self.malus_cause['Classes Gap'] += 1
                        self.malus_count += 1


    def compute_malus(self, Roster):
        """ Run required functions to compute student malus """
        self.student_timeslots(Roster)
        self.malus_points()