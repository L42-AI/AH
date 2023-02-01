"""
This file includes the class Student which represents each student.
The data used comes from the given dataframe.
add_courses and select_groups are part of the initialisation.
student_timeslot, malus_point are two methods to compute the malus points.
compute_malus runs these functions.
"""

import random

class Student():
    """This class represents a single student"""

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
        """ This function sets parameters used in pick_group """

        # If class is tutorial:
        if class_type == 'Tutorial':

            # Set all values of tutorial
            group_dict = course.tut_group_dict
            class_num = course.tutorials
            max_std = course.max_std_tutorial
            group = self.tut_group
        else:
            # Set all values of practica
            group_dict = course.pract_group_dict
            class_num = course.practicals
            max_std = course.max_std_practical
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
        """ This function selects groups of tutorial and practical for each course """

        self.tut_group = {}
        self.pract_group = {}

        # For each course
        for course in self.courses:

            # For each of the class types (with groups):
            for class_type in ['Tutorial', 'Practicals']:

                # Set the variable of the correct class
                group_dict, class_num, max_std, group = self.__set_type(course, class_type)

                # Run the pick group function
                self.__pick_group(course, group_dict, class_num, max_std, group)

    def __lecture_timeslot(self, course, current_course):
        """ This method adds the student Id's to the lectures """

        if course.lectures > 0:
            # For each lecture in the course:
            for index in range(course.lectures):

                # Set the current class
                current_lecture = f"lecture {index + 1}"

                # Add course and class to timeslot info
                current_course[current_lecture]['students'].add(self.id)

    def __pract_tut_timeslot(self, course, current_course, seminar_type):
        """ This method adds the student Id's to practicals or tutorials """

        #
        if seminar_type == "tutorial" and course.tutorials > 0:
            group = self.tut_group[course.name]

        elif seminar_type == "practical" and course.practicals > 0:
            group = self.pract_group[course.name]

        else:
            return "Error No Seminar of this type!"

        for index in range(eval(f"course.{seminar_type}s")):
            current_class = f"{seminar_type} {group + group * index}"
            current_course[current_class]['students'].add(self.id)

    def student_timeslots(self, Roster):
        """
        This method adds the timeslots for classes per week.
        The dictionary timeslots is linked to the Roster schedule.
        """

        # For each course:
        for course in self.courses:

            # Set the current course dict
            current_course = Roster.schedule[course.name]

            # Find and save the lecture timeslot
            self.__lecture_timeslot(course, current_course)

            # Find and save the tutorial timeslot
            self.__pract_tut_timeslot(course, current_course, 'tutorial')

            # Find and save the practicum timeslot
            self.__pract_tut_timeslot(course, current_course, 'practical')

    def __days_in_schedule(self, Roster):
        """ This method finds out how often a student has seminars in a day and appends it into the list for that day """

        # Create a days dictionary
        days = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}

        # For each course:
        for course in Roster.schedule:

            # For each class:
            for seminars in Roster.schedule[course]:

                # Set the class info
                class_info = Roster.schedule[course][seminars]

                # if the student follows that seminar
                if self.id in class_info['students']:

                    # Add the timeslots into the days dictionary
                    days[class_info['day']].append(class_info['timeslot'])
        return days

    def malus_points(self, Roster):
        """ This method calculates the malus points for the student """
        # Reset malus points to avoid summing dubble malus
        self.init_malus()

        # update the dictionary (later this should be linked to the roster schedule)'
        self.student_timeslots(Roster)

        # find how often student has classes per day
        days = self.__days_in_schedule(Roster)

        # go over the days
        for day in days:

            self.malus_cause['Tripple Gap'][day] = 0
            self.malus_cause['Classes Gap'][day] = 0
            self.malus_cause['Double Classes'][day] = 0

            # Sort the timeslots in the day:
            days[day] = sorted(days[day], reverse=True)

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
                        self.malus_cause['Double Classes'][day] += 1
                        self.malus_count += 1
                    else:
                        timeslots_double_classes.append(timeslot_list[timeslot_num])

                    # claculate the amount of gaps between lessons
                    if timeslot_list[timeslot_num] - timeslot_list[timeslot_num + 1] != 0:
                        lesson_gaps = int((timeslot_list[timeslot_num] - (timeslot_list[timeslot_num + 1] + 2)) / 2)

                        # check if one gap hour
                        if lesson_gaps == 1:
                            self.malus_cause['Classes Gap'][day] += 1
                            self.malus_count += 1

                        elif lesson_gaps == 2:
                            self.malus_cause['Classes Gap'][day] += 3
                            self.malus_count += 3

                        # we choose to give triple hours or more a value of 5, because it makes the data visibly more appealing
                        # and with this value the 'Tripple Gap' always convergace
                        elif lesson_gaps > 2:
                            self.malus_cause['Tripple Gap'][day] += 5
                            self.malus_count += 5