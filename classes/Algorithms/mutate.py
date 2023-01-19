
import random


class Mutate():
    def __init__(self, df, course_list, student_list, Roster):
        self.df = df
        self.course_list = course_list
        self.student_list = student_list
        self.Roster = Roster
        self.switched_student = None

    def __find_worst_student(self):
        """ This function returns the N worst students in terms of malus points """

        worst_student = max(self.student_list, key=lambda obj: obj.malus_count)
        return worst_student

    def __students_to_shuffle(self, student_list):
        """ This function goes through every student in the input list and shuffels them """

        # For each student:
        for student1 in student_list:

            # Find a second student
            for student2 in student_list:

                # Skip if the same student
                if student1 == student2:
                    continue

                # For each course
                for course in student1.courses:

                    # If course in other students course list
                    if course in student2.courses:

                        # Shuffle students
                        self.__shuffle(course, student1, student2)

    def __students_to_shuffle_random(self, s1):
        """ This function shuffles two random students """

        # Set a value that is not equal to enter while loop
        student1 = s1
        student2 = ''

        # While students are not equal
        while student1 != student2:

            # Randomly select students
            student2 = random.choice(self.student_list)

            # Randomly select a course from student1
            course = random.choice(student1.courses)

            # Skip if course not in other student
            if course not in student2.courses:
                continue

        # When different students found:
        self.__shuffle(course, student1, student2)

    def __shuffle(self, course, s1, s2):
        """ This function shuffles two students classes """

        def find_timeslots(course, s, class_type):
            """ This local function returns the timeslot of the student """

            # For each timeslot in the courses
            for timeslot in s.timeslots[course.name]:
                if timeslot.startswith(class_type):
                    return timeslot

        # take a random class types to change
        class_type = random.choice(['tutorial', 'practical'])

        if class_type == 'tutorial':
            group_dict = course.tut_group_dict
            max_std = course.max_std
        else:
            group_dict = course.pract_group_dict
            max_std = course.max_std_practica

        # Find timeslot
        s1_timeslot = find_timeslots(course, s1, class_type)
        s2_timeslot = find_timeslots(course, s2, class_type)


        for classes in self.Roster.schedule[course.name]:
            if classes.startswith(class_type):
                if self.Roster.schedule[course.name][s1_timeslot] != self.Roster.schedule[course.name][classes] and group_dict[int(classes[-1])] < max_std:
                    s1.timeslots[course.name][classes] = self.Roster.schedule[course.name][classes]
                    s1.timeslots[course.name].pop(s1_timeslot)

        # Skip if equal
        if s1_timeslot == s2_timeslot:
            return

        # Switch the timeslots
        s1.timeslots[course.name][s2_timeslot] = s2.timeslots[course.name][s2_timeslot]
        s2.timeslots[course.name][s1_timeslot] = s1.timeslots[course.name][s1_timeslot]

        # Delete the old timeslots
        s1.timeslots[course.name].pop(s1_timeslot)
        s2.timeslots[course.name].pop(s2_timeslot)

    def __set_type(self, course):

        # take a random class types to change
        class_type = random.choice(['tutorial', 'practical'])

        if class_type == 'tutorial':
            group_dict = course.tut_group_dict
            max_std = course.max_std
        else:
            group_dict = course.pract_group_dict
            max_std = course.max_std_practica

        return class_type, group_dict, max_std

    def __find_timeslots(self, course, s, class_type):
        """ This local function returns the timeslot of the student """

        # For each timeslot in the courses
        for timeslot in s.timeslots[course.name]:
            if timeslot.startswith(class_type):
                return timeslot

    def __change_class(self, s):
        """ This function shuffles two students classes """

        course = random.choice(self.course_list)

        while course.name not in list(s.timeslots.keys()):
            course = random.choice(self.course_list)

        # Set class type
        class_type, group_dict, max_std = self.__set_type(course)

        # Find timeslot
        s_timeslot = self.__find_timeslots(course, s, class_type)

        for classes in self.Roster.schedule[course.name]:
            if classes.startswith(class_type):

                if self.Roster.schedule[course.name][s_timeslot] != self.Roster.schedule[course.name][classes] and group_dict[int(classes[-1])] < max_std:

                    s.timeslots[course.name][classes] = self.Roster.schedule[course.name][classes]
                    s.timeslots[course.name].pop(s_timeslot)

                    group_dict[int(classes[-1])] += 1
                    group_dict[int(s_timeslot[-1])] -= 1
                    return


    def change_student_group(self):

        student = self.__find_worst_student()

        self.__change_class(student)


    def swap_2_students(self):

        switch_student_list = self.__find_worst_student()

        self.__students_to_shuffle(switch_student_list)

    # def swap_worst_students_random(self):


    def __swap_lecture(self, course):
        """
        This function takes in a list of object courses, a single object course and the object roster.
        It then takes a random course of the list courses and switches the lecture timeslots of the two.
        Because the roster schedule is changed, the student timeslots dictionary is changed as well.
        """

        # pick a random course to swap with that is not the same as as the course and the new course does have lectures
        random_course = random.choice([c for c in self.course_list if c != course and c.lectures > 0])

        # get all the lectures
        all_lectures_switch = [key for key in self.Roster.schedule[course.name].keys() if "lecture" in key]
        all_lectures_random = [key for key in self.Roster.schedule[random_course.name].keys() if "lecture" in key]

        # take a random lecture (if only one it will take the one)
        lecture_switch = random.choice(all_lectures_switch)
        lecture_random = random.choice(all_lectures_random)

        # define in order to be easier to read and switch key values
        dict_switch = self.Roster.schedule[course.name][lecture_switch]
        dict_random = self.Roster.schedule[random_course.name][lecture_random]

        # switch the times in the schedule roster
        self.Roster.schedule[course.name][lecture_switch] = dict(zip(dict_switch, dict_random.values()))
        self.Roster.schedule[random_course.name][lecture_random] = dict(zip(dict_random, dict_switch.values()))

    def swap_2_lectures(self):
        random_course = random.choice([c for c in self.course_list if c.lectures > 0])
        self.__swap_lecture(random_course)



    def __swap_lecture_empty_room(self, course):
        """
        This function takes in the roster object and a course. It then takes a random available room and
        switches the two rooms and timeslots. Each student roster is automatically changed as well,
        because their roster is linked to the roster schedule
        """

        # get all the lectures in the course and get all the empty rooms
        all_lectures_switch = [key for key in self.Roster.schedule[course.name].keys() if "lecture" in key]
        all_empty_rooms = [key for key in self.Roster.schedule['No course'].keys()]

        # choose a random lecture of that course
        lecture_switch = random.choice(all_lectures_switch)
        random_empty_room = random.choice(all_empty_rooms)

        # define in order to be easier to read and to be able to switch keys and values of the dict
        dict_switch = self.Roster.schedule[course.name][lecture_switch]
        dict_random = self.Roster.schedule['No course'][random_empty_room]

        # switch the times in the schedule roster
        self.Roster.schedule[course.name][lecture_switch] = dict(zip(dict_switch, dict_random.values()))
        self.Roster.schedule['No course'][random_empty_room] = dict(zip(dict_random, dict_switch.values()))

    def swap_lecture_empty_room(self):
        # pick a random course that which does have one or more lectures
        random_course = random.choice([c for c in self.course_list if c.lectures > 0])

        # call the swap function
        self.__swap_lecture_empty_room(random_course)

    def __pract_or_tut(self):
        picked = False
        while not picked:
            # pick random if tut or pract should be switched
            tut_or_pract = ['tut', 'pract']

            class_type = random.choice(tut_or_pract)
            

            # pick a random course that should switch
            course = random.choice(self.switch_student.courses)

            if course.tutorials > 0 and class_type == 'tut':
                picked = True
            if course.practica > 0 and class_type == 'pract':
                picked = True
        return course, class_type

    def __type_detect(self, class_type, course):

        if class_type == 'tut':
            course_group_type = course.tut_group_dict
            student_group = self.switch_student.tut_group[course.name]
        else:
            course_group_type = course.pract_group_dict
            student_group = self.switch_student.pract_group[course.name]
        return course_group_type, student_group
