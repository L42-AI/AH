
import random


class Mutate():
    def __init__(self, df, course_list, student_list, Roster):
        self.df = df
        self.course_list = course_list
        self.student_list = student_list
        self.Roster = Roster

    def __find_worst_students(self, num):
        """ This function returns the N worst students in terms of malus points """

        # Sort the Student Malus column
        self.df.sort_values(['Student Malus'], ascending=False, inplace=True)

        # Take N students
        worst_students = self.df['Student Object'].unique()[:num]
        return worst_students

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

        # Loop over the class types we want to change
        for class_type in ['tutorial', 'practical']:

            # Find timeslot
            s1_timeslot = find_timeslots(course, s1, class_type)
            s2_timeslot = find_timeslots(course, s2, class_type)

            # Skip if equal
            if s1_timeslot == s2_timeslot:
                continue

            # Switch the timeslots
            s1.timeslots[course.name][s2_timeslot] = s2.timeslots[course.name][s2_timeslot]
            s2.timeslots[course.name][s1_timeslot] = s1.timeslots[course.name][s1_timeslot]

            # Delete the old timeslots
            s1.timeslots[course.name].pop(s1_timeslot)
            s2.timeslots[course.name].pop(s2_timeslot)


    # def __shuffle(self, course, s1, s2):

    #     def compute_student_malus(self, s):
    #         s.compute_malus(self.Roster)
    #         return s.malus_count

    #     def set_tut_group(s):
    #         return s.tut_group[course.name]

    #     def set_pra_group(s):
    #         return s.pract_group[course.name]

    #     def shuffle_tutorial(course, s1, s2):
    #         if course.name in s1.tut_group:
    #             s1_tut_group = set_tut_group(s1)
    #             s2_tut_group = set_tut_group(s2)

    #             s1.tut_group[course.name] = s2_tut_group
    #             s2.tut_group[course.name] = s1_tut_group
    #         return s1_tut_group, s2_tut_group

    #     def shuffle_practicum(course, s1, s2):
    #         if course.name in s1.pract_group:
    #             s1_pra_group = set_pra_group(s1)
    #             s2_pra_group = set_pra_group(s2)

    #             s1.pract_group[course.name] = s2_pra_group
    #             s2.pract_group[course.name] = s1_pra_group
    #         return s1_pra_group, s2_pra_group

    #     def reset_shuffle(s1, s2, s1_tut_group, s2_tut_group, s1_pra_group, s2_pra_group):
    #         if course.name in s1.tut_group:
    #             s1.tut_group[course.name] = s1_tut_group
    #             s2.tut_group[course.name] = s2_tut_group
    #         if course.name in s1.pract_group:
    #             s1.pract_group[course.name] = s1_pra_group
    #             s2.pract_group[course.name] = s2_pra_group


    #     s1_old_malus = compute_student_malus(self, s1)
    #     s2_old_malus = compute_student_malus(self, s2)

    #     s1_tut_group, s2_tut_group = shuffle_tutorial(course, s1, s2)
    #     s1_pra_group, s2_pra_group = shuffle_practicum(course, s1, s2)

    #     s1_new_malus = compute_student_malus(self, s1)
    #     s2_new_malus = compute_student_malus(self, s2)

    #     s1_difference = s1_new_malus - s1_old_malus
    #     s2_difference = s2_new_malus - s2_old_malus

    #     if s1_difference + s2_difference < 0:
    #         s1_old_malus = s1_new_malus
    #         s2_old_malus = s2_new_malus
    #     else:
    #         reset_shuffle(s1, s2, s1_tut_group, s2_tut_group, s1_pra_group, s2_pra_group)


    def swap_2_students(self, num = 100):

        switch_student_list = self.__find_worst_students(num)

        self.__students_to_shuffle(switch_student_list)

    def swap_2_students_random(self):

        self.__students_to_shuffle_random()

    def swap_2_lectures(self):

        # pick two random courses that have at least one lecture
        random_course_1, random_course_2 = random.sample([c for c in self.course_list if c.lectures > 0], 2)

        # get all the lectures
        all_lectures_random_1 = [key for key in self.Roster.schedule[random_course_1.name].keys() if "lecture" in key]
        all_lectures_random_2 = [key for key in self.Roster.schedule[random_course_2.name].keys() if "lecture" in key]

        # take a random lecture (if only one it will take the one)
        lecture_random_1 = random.choice(all_lectures_random_1)
        lecture_random_2 = random.choice(all_lectures_random_2)

        # define in order to be easier to read and switch key values
        dict_random_1 = self.Roster.schedule[random_course_1.name][lecture_random_1]
        dict_random_2 = self.Roster.schedule[random_course_2.name][lecture_random_2]

        # switch the times in the schedule roster
        self.Roster.schedule[random_course_1.name][lecture_random_1] = dict(zip(dict_random_1, dict_random_2.values()))
        self.Roster.schedule[random_course_2.name][lecture_random_2] = dict(zip(dict_random_2, dict_random_1.values()))
        
    def swap_lecture_empty_room(self):
        """
        This function takes in the roster object and a course. It then takes a random available room and
        switches the two rooms and timeslots. Each student roster is automatically changed as well,
        because their roster is linked to the roster schedule
        """

        # pick a random course that which does have one or more lectures
        random_course = random.choice([c for c in self.course_list if c.lectures > 0])

        # get all the lectures in the course and get all the empty rooms
        all_lectures_switch = [key for key in self.Roster.schedule[random_course.name].keys() if "lecture" in key]
        all_empty_rooms = [key for key in self.Roster.schedule['No course'].keys()]

        # choose a random lecture of that course
        lecture_switch = random.choice(all_lectures_switch)
        random_empty_room = random.choice(all_empty_rooms)

        # define in order to be easier to read and to be able to switch keys and values of the dict
        dict_switch = self.Roster.schedule[random_course.name][lecture_switch]
        dict_random = self.Roster.schedule['No course'][random_empty_room]

        # switch the times in the schedule roster
        self.Roster.schedule[random_course.name][lecture_switch] = dict(zip(dict_switch, dict_random.values()))
        self.Roster.schedule['No course'][random_empty_room] = dict(zip(dict_random, dict_switch.values()))

    def swap_2_tutorials(self):

        # pick two random courses that have at least one lecture
        random_course_1, random_course_2 = random.sample([c for c in self.course_list if c.tutorials > 0], 2)

        # get all the lectures
        all_tutorial_random_1 = [key for key in self.Roster.schedule[random_course_1.name].keys() if "tutorial" in key]
        all_tutorial_random_2 = [key for key in self.Roster.schedule[random_course_2.name].keys() if "tutorial" in key]

        # take a random lecture (if only one it will take the one)
        tutorial_random_1 = random.choice(all_tutorial_random_1)
        tutorial_random_2 = random.choice(all_tutorial_random_2)

        # define in order to be easier to read and switch key values
        dict_random_1 = self.Roster.schedule[random_course_1.name][tutorial_random_1]
        dict_random_2 = self.Roster.schedule[random_course_2.name][tutorial_random_2]

        # switch the times in the schedule roster
        self.Roster.schedule[random_course_1.name][tutorial_random_1] = dict(zip(dict_random_1, dict_random_2.values()))
        self.Roster.schedule[random_course_2.name][tutorial_random_2] = dict(zip(dict_random_2, dict_random_1.values()))

    def swap_tutorial_empty_room(self):
        # pick a random course that which does have one or more lectures
        random_course = random.choice([c for c in self.course_list if c.tutorials > 0])

        # get all the tutorials in the course and get all the empty rooms
        all_lectures_switch = [key for key in self.Roster.schedule[random_course.name].keys() if "tutorial" in key]
        all_empty_rooms = [key for key in self.Roster.schedule['No course'].keys()]

        # choose a random lecture of that course
        lecture_switch = random.choice(all_lectures_switch)
        random_empty_room = random.choice(all_empty_rooms)

        # define in order to be easier to read and to be able to switch keys and values of the dict
        dict_switch = self.Roster.schedule[random_course.name][lecture_switch]
        dict_random = self.Roster.schedule['No course'][random_empty_room]

        # switch the times in the schedule roster
        self.Roster.schedule[random_course.name][lecture_switch] = dict(zip(dict_switch, dict_random.values()))
        self.Roster.schedule['No course'][random_empty_room] = dict(zip(dict_random, dict_switch.values()))

    def swap_2_practicals(self):

        # pick two random courses that have at least one lecture
        random_course_1, random_course_2 = random.sample([c for c in self.course_list if c.practicals > 0], 2)

        # get all the lectures
        all_tutorial_random_1 = [key for key in self.Roster.schedule[random_course_1.name].keys() if "practical" in key]
        all_tutorial_random_2 = [key for key in self.Roster.schedule[random_course_2.name].keys() if "practical" in key]

        # take a random lecture (if only one it will take the one)
        tutorial_random_1 = random.choice(all_tutorial_random_1)
        tutorial_random_2 = random.choice(all_tutorial_random_2)

        # define in order to be easier to read and switch key values
        dict_random_1 = self.Roster.schedule[random_course_1.name][tutorial_random_1]
        dict_random_2 = self.Roster.schedule[random_course_2.name][tutorial_random_2]

        # switch the times in the schedule roster
        self.Roster.schedule[random_course_1.name][tutorial_random_1] = dict(zip(dict_random_1, dict_random_2.values()))
        self.Roster.schedule[random_course_2.name][tutorial_random_2] = dict(zip(dict_random_2, dict_random_1.values()))

    def swap_practical_empty_room(self):

        # pick a random course that which does have one or more lectures
        random_course = random.choice([c for c in self.course_list if c.practicals > 0])

        # get all the tutorials in the course and get all the empty rooms
        all_lectures_switch = [key for key in self.Roster.schedule[random_course.name].keys() if "practical" in key]
        all_empty_rooms = [key for key in self.Roster.schedule['No course'].keys()]

        # choose a random lecture of that course
        lecture_switch = random.choice(all_lectures_switch)
        random_empty_room = random.choice(all_empty_rooms)

        # define in order to be easier to read and to be able to switch keys and values of the dict
        dict_switch = self.Roster.schedule[random_course.name][lecture_switch]
        dict_random = self.Roster.schedule['No course'][random_empty_room]

        # switch the times in the schedule roster
        self.Roster.schedule[random_course.name][lecture_switch] = dict(zip(dict_switch, dict_random.values()))
        self.Roster.schedule['No course'][random_empty_room] = dict(zip(dict_random, dict_switch.values()))

    def test_swap_empty(self, lesson_type):

         # pick a random course that does have one or more lessons of said type
        random_course = random.choice([c for c in self.course_list if getattr(c, f'{lesson_type}s') > 0])

        # get all the tutorials in the course and get all the empty rooms
        all_lectures_switch = [key for key in self.Roster.schedule[random_course.name].keys() if lesson_type in key]
        all_empty_rooms = [key for key in self.Roster.schedule['No course'].keys()]

        # choose a random lecture of that course
        lecture_switch = random.choice(all_lectures_switch)
        random_empty_room = random.choice(all_empty_rooms)

        # define in order to be easier to read and to be able to switch keys and values of the dict
        dict_switch = self.Roster.schedule[random_course.name][lecture_switch]
        dict_random = self.Roster.schedule['No course'][random_empty_room]

        # switch the times in the schedule roster
        self.Roster.schedule[random_course.name][lecture_switch] = dict(zip(dict_switch, dict_random.values()))
        self.Roster.schedule['No course'][random_empty_room] = dict(zip(dict_random, dict_switch.values()))

    def test_swap_2_lessons(self, lesson_type):

        # pick two random courses that have at least one lecture
        random_course_1, random_course_2 = random.sample([c for c in self.course_list if c.practicals > 0], 2)

        # get all the lectures
        all_tutorial_random_1 = [key for key in self.Roster.schedule[random_course_1.name].keys() if lesson_type in key]
        all_tutorial_random_2 = [key for key in self.Roster.schedule[random_course_2.name].keys() if lesson_type in key]

        # take a random lecture (if only one it will take the one)
        tutorial_random_1 = random.choice(all_tutorial_random_1)
        tutorial_random_2 = random.choice(all_tutorial_random_2)

        # define in order to be easier to read and switch key values
        dict_random_1 = self.Roster.schedule[random_course_1.name][tutorial_random_1]
        dict_random_2 = self.Roster.schedule[random_course_2.name][tutorial_random_2]

        # switch the times in the schedule roster
        self.Roster.schedule[random_course_1.name][tutorial_random_1] = dict(zip(dict_random_1, dict_random_2.values()))
        self.Roster.schedule[random_course_2.name][tutorial_random_2] = dict(zip(dict_random_2, dict_random_1.values()))
        