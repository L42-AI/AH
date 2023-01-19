
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

    def swap_worst_student(self):

        # find student with highest malus
        self.switch_student = self.__find_worst_student()
        print(self.switch_student.id)

        # pick a tutorial or practical to switch
        course, class_type = self.__pract_or_tut()

        # check if tut or pract group is needed
        course_group_type, student_group = self.__type_detect(class_type, course)


        # pick a group to switch to
        groups = list(course_group_type.keys())
        group_to_switch_to = random.choice(groups)

        # check if student is not already in it
        if group_to_switch_to != student_group:
            # check if there is room, given the type of the class
            if course_group_type[group_to_switch_to] < course.max_std and class_type == 'tut':
                course_group_type[group_to_switch_to] += 1
                course_group_type[student_group] -= 1
                self.switch_student.tut_group[course.name] = group_to_switch_to
                self.switch_student.student_timeslots(self.Roster)

            if course_group_type[group_to_switch_to] < course.max_std_practica and class_type == 'pract':
                course_group_type[group_to_switch_to] += 1
                course_group_type[student_group] -= 1
                self.switch_student.pract_group[course.name] = group_to_switch_to
                self.switch_student.student_timeslots(self.Roster)


            # if there is no room, switch students
            if course_group_type[group_to_switch_to] == course.max_std and class_type == 'tut':
                possible_students = {}
                for student in course.enrolled_students:
                    if student.tut_group[course.name] == group_to_switch_to:
                        possible_students[student] = student.malus_count
                
                        # find worst student in that group
                        worst_student = max(possible_students, key=possible_students.get)

                        # switch students
                        worst_student.tut_group[course.name] = self.switch_student.tut_group[course.name]
                        self.switch_student.tut_group[course.name] = group_to_switch_to
                        self.switch_student.student_timeslots(self.Roster)
                        worst_student.student_timeslots(self.Roster)


            if course_group_type[group_to_switch_to] == course.max_std_practica and class_type == 'pract':
                possible_students = {}
                for student in course.enrolled_students:
                    if student.pract_group[course.name] == group_to_switch_to:
                        possible_students[student] = student.malus_count
                
                # find worst student in that group
                worst_student = max(possible_students, key=possible_students.get)

                # switch students
                worst_student.pract_group[course.name] = self.switch_student.pract_group[course.name]
                self.switch_student.pract_group[course.name] = group_to_switch_to
                self.switch_student.student_timeslots(self.Roster)
                worst_student.student_timeslots(self.Roster)



    def swap_worst_students_random(self):

        self.__students_to_shuffle_random()

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
