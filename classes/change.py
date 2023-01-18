import random

class Change():
    def __init__(self, df, course_list, student_list, Roster):
        self.df = df
        self.course_list = course_list
        self.student_list = student_list
        self.Roster = Roster
        pass

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

    def __shuffle(self, course, student1, student2):

        student1.compute_malus(self.Roster)
        student2.compute_malus(self.Roster)

        student1_old_malus = student1.malus_count
        student2_old_malus = student2.malus_count

        # Set group
        if course.name in student1.tut_group:
            student1_tutorial_group = student1.tut_group[course.name]
            student2_tutorial_group = student2.tut_group[course.name]

            student1.tut_group[course.name] = student2_tutorial_group
            student2.tut_group[course.name] = student1_tutorial_group

        if course.name in student1.pract_group:
            student1_practicum_group = student1.pract_group[course.name]
            student2_practicum_group = student2.pract_group[course.name]

            student1.pract_group[course.name] = student2_practicum_group
            student2.pract_group[course.name] = student1_practicum_group

        student1.compute_malus(self.Roster)
        student2.compute_malus(self.Roster)

        student1_new_malus = student1.malus_count
        student2_new_malus = student2.malus_count

        student1_difference = student1_new_malus - student1_old_malus
        student2_difference = student2_new_malus - student2_old_malus

        if student1_difference + student2_difference < 0:
            student1_old_malus = student1_new_malus
            student2_old_malus = student2_new_malus
        else:
            if course.name in student1.tut_group:
                student1.tut_group[course.name] = student1_tutorial_group
                student2.tut_group[course.name] = student2_tutorial_group
            if course.name in student1.pract_group:
                student1.pract_group[course.name] = student1_practicum_group
                student2.pract_group[course.name] = student2_practicum_group

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
        for course in self.course_list:
            if course.lectures > 0:
                self.__swap_lecture(course)

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
        for course in self.course_list:
            if course.lecture > 0:
                self.__swap_lecture_empty_room(course)
