class Change():
    def __init__(self, df, course_list, student_list, Roster):
        self.df = df
        self.course_list = course_list
        self.student_list = student_list
        self.Roster = Roster
        pass

    def find_worst_students(self, num):
        self.df.sort_values(['Student Malus'], ascending=False, inplace=True)
        worst_students = self.df['Object'].unique()[:num]
        return worst_students

    def shuffle_students(self, student_list, space_dict):

        for i in range(len(student_list) - 1):

            student_1 = student_list[i]
            student_2 = student_list[i + 1]

            for course in student_1.courses:

                if course in student_2.courses:
                    self.shuffle(course, student_1, student_2)

    def test_classses(self, timeslot):

        switch_dict = {}

        for classes in self.Roster.schedule[course]:
            student.timeslots[course] = self.Roster.schedule[course][classes]
            student.malus_points()
            switch_dict[classes] = student.malus_count

            lowest_malus_class = min(switch_dict.items(), key=lambda x: x[1])[0]
            print(lowest_malus_class)
            student.timeslots[course] = self.Roster.schedule[course][lowest_malus_class]

        return switch_dict

    def shuffle(self, course, student1, student2):
        course






        return



    def switch_students(self, num = 10):

        switch_student_list = self.find_worst_students(num)

        self.shuffle_students(switch_student_list)



        def shuffle_tut(class_indexes, student, course, space_dict, Roster):

            print('TUT')
            print(student.tut_group[course.name])
            print()

            free_tutorials = []
            for class_group in space_dict[course.name]:
                if class_group.startswith('Tutorial'):
                    free_tutorials.append(class_group[-1])

            for i in class_indexes:

                timeslot = student.timeslots[i]


                if timeslot['class'].startswith('tutorial'):

                    print(f'length of student timeslot list: {len(student.timeslots)}')

                    student.timeslots.remove(timeslot)

                    for tutorial in free_tutorials:

                        print('MALUS POINTS')
                        print(student.malus_count)

                        student.tut_group[course.name] = tutorial
                        timeslot_dict = student.tutorial_timeslot(course, Roster.schedule[course.name])
                        student.timeslots.append(timeslot_dict)
                        student.malus_points()
                        student.timeslots.remove(timeslot_dict)

            return


        pass

    def switch_classes(self):
        pass