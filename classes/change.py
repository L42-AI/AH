
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

        print('COURSE:')
        print(course)
        print()

        student1.malus_points()
        student2.malus_points()

        student1_old_malus = student1.malus_count
        student2_old_malus = student2.malus_count

        print(f'Student1 old malus: {student1_old_malus}')
        print(f'Student2 old malus: {student2_old_malus}')

        for type in ['tutorial', 'practical']:

            student1_possible_classes = [key for key in student1.timeslots[course.name].keys() if key.startswith(type)]
            student2_possible_classes = [key for key in student2.timeslots[course.name].keys() if key.startswith(type)]

            # If group of both students is the same group, skip
            if student1_possible_classes == student2_possible_classes:
                continue

            print(student2_possible_classes)
            print(student1_possible_classes)

            print(student2.timeslots[course.name][student2_possible_classes[0]])
            print(student1.timeslots[course.name][student1_possible_classes[0]])



            for student1_classes in student1_possible_classes:
                for student2_classes in student2_possible_classes:

                    if student1_classes not in student2.timeslots[course.name]:
                        student2.timeslots[course.name][student1_classes] = student1.timeslots[course.name][student1_classes]

                    if student2_classes not in student1.timeslots[course.name]:
                        student1.timeslots[course.name][student2_classes] = student2.timeslots[course.name][student2_classes]

                    if student2_classes in student2.timeslots[course.name]:
                        student2.timeslots[course.name].pop(student2_classes)

                    if student1_classes in student1.timeslots[course.name]:
                        student1.timeslots[course.name].pop(student1_classes)

                    student1.malus_points()
                    student2.malus_points()

                    student1_new_malus = student1.malus_count
                    student2_new_malus = student2.malus_count

                    print(f'Student1 new malus: {student1_new_malus}')
                    print(f'Student2 new malus: {student2_new_malus}')

                    student1_difference = student1_new_malus - student1_old_malus
                    student2_difference = student2_new_malus - student2_old_malus

                    print(student1_difference)
                    print(student2_difference)

                    print(student2.timeslots[course.name][student1_possible_classes[0]])
                    print(student1.timeslots[course.name][student2_possible_classes[0]])

                    if student1_difference + student2_difference < 0:
                        student1_old_malus = student1_new_malus
                        student2_old_malus = student2_new_malus
                    else:

                        if student2_classes in student2.timeslots[course.name]:
                            student2.timeslots[course.name][student2_classes] = student1.timeslots[course.name][student1_classes]

                        if student2_classes not in student1.timeslots[course.name]:
                            student1.timeslots[course.name][student1_classes] = student2.timeslots[course.name][student2_classes]

                        if student2_classes in student2.timeslots[course.name]:
                            student2.timeslots[course.name].pop(student1_classes)

                        if student1_classes in student1.timeslots[course.name]:
                            student1.timeslots[course.name].pop(student2_classes)

    def switch_2_students(self, num = 100):

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
        lecture_switch = [key for key in self.Roster.schedule[course.name].keys() if "lecture" in key]
        lecture_random = [key for key in self.Roster.schedule[random_course.name].keys() if "lecture" in key]

        # take a random lecture (if only one it will take the one)
        lecture_switch = random.choice(lecture_switch)
        lecture_random = random.choice(lecture_random)

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