
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

        worst_student = sorted(self.student_list, key=lambda obj: obj.malus_count)[:10]
        return worst_student

    def __find_random_student(self):
        """ This function returns a random student from the list students """

        return random.choice(self.student_list)

    def __students_to_shuffle(self, student_list):
        """ This function goes through every student in the input list and shuffels them """

        # For each student:
        for student1 in student_list:

            # Find a second student beside the first student
            for student2 in (s for s in student_list if s != student1):

                # For each course
                for course in student1.courses:

                    # If course in other students course list
                    if course in student2.courses:

                        # Shuffle students
                        self.__shuffle(course, student1, student2)

    def __students_to_shuffle_random(self):
        """ This function shuffles two random students """

        # Set a value that is not equal to enter while loop
        student1 = 'a'
        student2 = 'b'

        # While students are not equal
        while student1 != student2:

            # Randomly select students
            student1 = random.choice(self.student_list)
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

        # Find timeslot
        s1_timeslot = find_timeslots(course, s1, class_type)
        s2_timeslot = find_timeslots(course, s2, class_type)

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
            max_std = course.max_std_practical

        return class_type, group_dict, max_std

    def __find_timeslots(self, course, s, class_type):
        """ This local function returns the timeslot of the student """

        # For each timeslot in the courses
        for timeslot in s.timeslots[course.name]:
            if timeslot.startswith(class_type):
                return timeslot

    def __change_group(self, s):
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

        student = self.__find_random_student()

        self.__change_group(student)


    def swap_2_students(self):

        switch_student_list = self.__find_worst_student()

        self.__students_to_shuffle(switch_student_list)

    def swap_2_students_random(self):

        self.__students_to_shuffle_random()

    # def swap_lessons(self, lesson_type, empty):
    #     """
    #     This function swaps two of the same lesson_type with the help of two input variables. 
    #     Lesson type is a string of they type of lesson for example tutorial.
    #     The second variable is a boolean whether you want to swap with an empty room or not. If empty is set to Fals
    #     you swap the lesson with a random other lesson. If it is True you swap with an empty room.
    #     """

    #     # check if you swap with an empty room or another course
    #     if empty:
    #         # pick a random course that does have one or more lessons of said type
    #         random_course_1 = random.choice([c for c in self.course_list if getattr(c, f'{lesson_type}s') > 0])
            
    #         all_lessons_random_2 = [key for key in self.Roster.schedule['No course'].keys()]

    #         course_two = 'No course'
        
    #     else:
    #         # pick random lesson that has at leas one of the lesson type
    #         random_course_1, random_course_2 = random.sample([c for c in self.course_list if getattr(c, f'{lesson_type}s') > 0], 2)
    #         all_lessons_random_2 = [key for key in self.Roster.schedule[random_course_2.name].keys() if lesson_type in key]
    #         course_two = random_course_2.name
        
    #     # get all the tutorials in the course and get all the empty rooms
    #     all_lessons_random_1 = [key for key in self.Roster.schedule[random_course_1.name].keys() if lesson_type in key]

    #     # choose a random lecture of that course
    #     lesson_1 = random.choice(all_lessons_random_1)
    #     lesson_2 = random.choice(all_lessons_random_2)

    #     # define in order to be easier to read and to be able to switch keys and values of the dict
    #     dict_1 = self.Roster.schedule[random_course_1.name][lesson_1]
    #     dict_2 = self.Roster.schedule[course_two][lesson_2]

    #     # switch the times in the schedule roster
    #     self.Roster.schedule[random_course_1.name][lesson_1] = dict(zip(dict_1, dict_2.values()))
    #     self.Roster.schedule[course_two][lesson_2] = dict(zip(dict_2, dict_1.values()))

    def swap_random_lessons(self, empty):

        # check if you want to swap with an empty room or not
        if empty:
            # get one random course and all the empty room time slots
            random_course_1 = random.choice(self.course_list)
            all_lessons_random_2 = [key for key in self.Roster.schedule['No course'].keys()]
            course_two = 'No course'

        else:
            # get two random courses
            random_course_1, random_course_2 = random.sample(self.course_list, 2)
            all_lessons_random_2 = list(self.Roster.schedule[random_course_2.name].keys())
            course_two = random_course_2.name

        # get all the lessons in that course
        all_lessons_random_1 = list(self.Roster.schedule[random_course_1.name].keys())

        # choose two random lessons
        lesson_1 = random.choice(all_lessons_random_1)
        lesson_2 = random.choice(all_lessons_random_2)

        # define in order to be easier to read and to be able to switch keys and values of the dict
        dict_1 = self.Roster.schedule[random_course_1.name][lesson_1]
        dict_2 = self.Roster.schedule[course_two][lesson_2]

        # switch the times in the schedule roster
        self.Roster.schedule[random_course_1.name][lesson_1] = dict(zip(dict_1, dict_2.values()))
        self.Roster.schedule[course_two][lesson_2] = dict(zip(dict_2, dict_1.values()))

    # def __pract_or_tut(self):
    #     picked = False
    #     while not picked:
    #         # pick random if tut or pract should be switched
    #         tut_or_pract = ['tut', 'pract']

    #         class_type = random.choice(tut_or_pract)

    #         # pick a random course that should switch
    #         course = random.choice(self.switch_student.courses)

    #         if course.tutorials > 0 and class_type == 'tut':
    #             picked = True
    #         if course.practica > 0 and class_type == 'pract':
    #             picked = True
    #     return course, class_type

    # def __type_detect(self, class_type, course):

    #     if class_type == 'tut':
    #         course_group_type = course.tut_group_dict
    #         student_group = self.switch_student.tut_group[course.name]
    #     else:
    #         course_group_type = course.pract_group_dict
    #         student_group = self.switch_student.pract_group[course.name]
    #     return course_group_type, student_group

    # def __pract_or_tut(self):
    #     picked = False
    #     while not picked:
    #         # pick random if tut or pract should be switched
    #         tut_or_pract = ['tut', 'pract']

    #         class_type = random.choice(tut_or_pract)
            

    #         # pick a random course that should switch
    #         course = random.choice(self.switch_student.courses)

    #         if course.tutorials > 0 and class_type == 'tut':
    #             picked = True
    #         if course.practica > 0 and class_type == 'pract':
    #             picked = True
    #     return course, class_type

    # def __type_detect(self, class_type, course):

    #     if class_type == 'tut':
    #         course_group_type = course.tut_group_dict
    #         student_group = self.switch_student.tut_group[course.name]
    #     else:
    #         course_group_type = course.pract_group_dict
    #         student_group = self.switch_student.pract_group[course.name]
    #     return course_group_type, student_group
