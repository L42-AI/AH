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
        self.courses = []
        self.add_courses(courses)

        # Make dictionaries for practicum and tutorial groups
        self.tut_group = {}
        self.pract_group = {}
        self.select_groups()

        # Make list of timeslots
        self.timeslots = []

        # Set malus point dict
        self.malus = {}
        self.init_malus()

    # def __str__(self):
    #     return f"{self.f_name} {self.l_name}"

    def init_malus(self):
        self.malus['Classes Gap'] = 0

    def add_courses(self, courses):
        """ Assign all the courses to the student and set the enrollment dictionary """

        # For each course:
        for name in self.courses_names:

            # Add courses to the courses list
            for course in courses:
                if course.name == name:
                    self.courses.append(course)

    def set_type(self, course, class_type):
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

    def pick_group(self, course, group_dict, class_num, max_std, group):
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

        # For each course
        for course in self.courses:

            # For each of the class types (with groups):
            for class_type in ['Tutorial', 'Practica']:

                # Set the variable of the correct class
                group_dict, class_num, max_std, group = self.set_type(course, class_type)

                # Run the pick group function
                self.pick_group(course, group_dict, class_num, max_std, group)

    def student_timeslots(self, Roster):
        """ This method adds the timeslots for classes per week """

        # Go over all courses:
        for course in self.courses:

            current_course = Roster.schedule[course.name]

            # For each lecture in the course:
            for index in range(course.lectures):

                # Set the current class
                current_lecture = f"lecture {index + 1}"

                # Add course and class to timeslot info
                timeslot_dict = current_course[current_lecture]
                timeslot_dict['course'] = course.name
                timeslot_dict['class'] = current_lecture

                # Add the class to the timeslots of the student (Every student attends all lectures)
                self.timeslots.append(timeslot_dict)

            # For each tutorial in the course:
            for index in range(course.tutorials):

                # Set the current class
                current_tutorial = f"tutorial {(self.tut_group[course.name] + self.tut_group[course.name] * index)}"

                # Add course and class to timeslot info
                timeslot_dict = current_course[current_tutorial]
                timeslot_dict['course'] = course.name
                timeslot_dict['class'] = current_tutorial

                # Add the tutorial where the student is enrolled to the timeslots of the student # Ask Jacob
                # tut*index is incase group needs 2 tutorials, so they need timeslots from 2 entries
                self.timeslots.append(timeslot_dict)

            # For each practicum in the course:
            for index in range(course.practica):

                # Set the current class
                current_practicum = f"practical {(self.pract_group[course.name] + self.pract_group[course.name] * index)}"

                # Add course and class to timeslot info
                timeslot_dict = current_course[current_practicum]
                timeslot_dict['course'] = course.name
                timeslot_dict['class'] = current_practicum

                # Add the practicum where the student is enrolled to the timeslots of the student
                self.timeslots.append(timeslot_dict)

    def malus_points(self):
        """ This method calculates the malus points point for the student """

        # Reset malus points to avoid summing dubble malus
        self.init_malus()

        # Create a days dictionary
        days = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}

        # For each timeslot:
        for timeslot in self.timeslots:

            # Add the timeslots into the days dictionary
            days[timeslot['day']].append(timeslot['timeslot'])

        # For each day in days:
        for day in days:

            # Sort the timeslots in the day:
            days[day].sort(reverse=True)

            # Set the dictionary key as list
            timeslot_list = days[day]

            # Only compute if list includes more than 1 timeslot
            if len(timeslot_list) > 1:

                # For each timeslot number: (range is -1 to ensure the use of index + 1)
                for timeslot_num in range(len(timeslot_list) - 1):

                    # some cases, double booking might be allowed, but we do not want to add 2 malus
                    if timeslot_list[timeslot_num] - timeslot_list[timeslot_num + 1] != 0:
                        self.malus['Classes Gap'] += int((timeslot_list[timeslot_num] - (timeslot_list[timeslot_num + 1] + 2)) / 2)
                    else:
                        self.malus['Classes Gap'] += 1

    def compute_malus(self, Roster):
        """ Run required functions to compute student malus """
        self.student_timeslots(Roster)
        self.malus_points()