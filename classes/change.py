class Change():
    def __init__(self, df, course_list, student_list, Roster):
        self.df = df
        self.course_list = course_list
        self.student_list = student_list
        self.Roster = Roster
        pass

    def __find_worst_students(self, num):
        self.df.sort_values(['Student Malus'], ascending=False, inplace=True)
        worst_students = self.df['Object'].unique()[:num]
        return worst_students

    def __students_to_shuffle(self, student_list):

        for i in range(len(student_list) - 1):

            student_1 = student_list[i]
            student_2 = student_list[i + 1]

            for course in student_1.courses:

                if course in student_2.courses:
                    self.__shuffle(course, student_1, student_2)

    def __shuffle(self, course, student1, student2):

        student1.malus_points()
        student2.malus_points()

        student1_old_malus = student1.malus_count
        student2_old_malus = student2.malus_count

        print(f'Student1 old malus: {student1_old_malus}')
        print(f'Student2 old malus: {student2_old_malus}')

        for type in ['tutorial', 'practical']:
            for class_type in student1.timeslots[course.name]:
                print(course)
                print()

                if class_type.startswith(type):

                    student1_possible_classes = [key for key in student1.timeslots[course.name].keys() if key.startswith(type)]
                    student2_possible_classes = [key for key in student2.timeslots[course.name].keys() if key.startswith(type)]

                    for student1_classes in student1_possible_classes:
                        for student2_classes in student2_possible_classes:

                            if student1_classes == student2_classes:
                                continue

                            student1_class = student1.timeslots[course.name][student1_classes]
                            student2_class = student2.timeslots[course.name][student2_classes]
                            print(student1_class)
                            print(student2_class)

                            student1.timeslots[course.name][student1_classes] = student2.timeslots[course.name][student2_classes]
                            student2.timeslots[course.name][student2_classes] = student1.timeslots[course.name][student1_classes]

                            student1.malus_points()
                            student2.malus_points()

                            student1_new_malus = student1.malus_count
                            student2_new_malus = student2.malus_count

                            if student1_new_malus < student1_old_malus and student2_new_malus < student2_old_malus:
                                student1_old_malus = student1_new_malus
                                student2_old_malus = student2_new_malus
                            else:
                                student1.timeslots[course.name][class_type] = student2.timeslots[course.name][classes]
                                student2.timeslots[course.name][class_type] = student1.timeslots[course.name][classes]

    def switch_2_students(self, num = 100):

        switch_student_list = self.__find_worst_students(num)

        self.__students_to_shuffle(switch_student_list)
