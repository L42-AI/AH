
import random


class Change():
    def __init__(self, df, course_list, student_list, Roster):
        self.df = df
        self.course_list = course_list
        self.student_list = student_list
        self.Roster = Roster

    def __find_worst_students(self, num):
        self.df.sort_values(['Student Malus'], ascending=False, inplace=True)
        worst_students = self.df['Student Object'].unique()[:num]
        return worst_students

    def __students_to_shuffle(self, student_list):
        for student1 in student_list:
            for student2 in student_list:
                if student1 == student2:
                    continue

                for course in student1.courses:
                    if course in student2.courses:

                        self.__shuffle(course, student1, student2)

    def __shuffle(self, course, s1, s2):

        def shuffle_tutorial(self, course, s1, s2):
            pass

        def shuffle_practicum(self, course, s1, s2):
            pass

        def compute_student_malus(self, s):
            s.compute_malus(self.Roster)
            return s.malus_count

        def set_tut_group(s):
            return s.tut_group[course.name]

        def set_pra_group(s):
            return s.pract_group[course.name]

        s1_old_malus = compute_student_malus(self, s1)
        s2_old_malus = compute_student_malus(self, s2)

        # Set group
        if course.name in s1.tut_group:
            s1_tut_group = set_tut_group(s1)
            s2_tut_group = set_tut_group(s2)

            s1.tut_group[course.name] = s2_tut_group
            s2.tut_group[course.name] = s1_tut_group

        if course.name in s1.pract_group:
            s1_pra_group = set_pra_group(s1)
            s2_pra_group = set_pra_group(s2)

            s1.pract_group[course.name] = s2_pra_group
            s2.pract_group[course.name] = s1_pra_group

        s1_new_malus = compute_student_malus(self, s1)
        s2_new_malus = compute_student_malus(self, s2)

        s1_difference = s1_new_malus - s1_old_malus
        s2_difference = s2_new_malus - s2_old_malus

        if s1_difference + s2_difference < 0:
            s1_old_malus = s1_new_malus
            s2_old_malus = s2_new_malus
        else:
            if course.name in s1.tut_group:
                s1.tut_group[course.name] = s1_tut_group
                s2.tut_group[course.name] = s2_tut_group
            if course.name in s1.pract_group:
                s1.pract_group[course.name] = s1_pra_group
                s2.pract_group[course.name] = s2_pra_group


    def swap_2_students(self, num = 100):

        switch_student_list = self.__find_worst_students(num)

        self.__students_to_shuffle(switch_student_list)


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
