
import random


class Mutate():
    def __init__(self, df, course_list, student_list, Roster):
        self.df = df
        self.course_list = course_list
        self.student_list = student_list
        self.Roster = Roster
        self.switched_student = None

        # dict with student and course objects with one attribute as value
        # makes searching them based on that attribute faster
        self.student_dict = {}
        self.__create_student_id_dict()
        self.course_dict = {}
        self.__create_course_name_dict()
        

    def __find_worst_student(self):
        """ This function returns the N worst students in terms of malus points """

        worst_student = sorted(self.student_list, key=lambda obj: obj.malus_count)[0]
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
        
    def swap_timeslots(self):
        worst_student = self.__find_worst_student()


    def swap_timeslots(self):
        worst_student = self.__find_worst_student()

    def swap_bad_timeslots(self):
        
        # pick a student to switch
        student_to_switch = self.__find_random_student()

        # find its worst day
        worst_day = self.__worst_day(student_to_switch)
    
        # find classes that day
        class_to_switch, course = self.__find_classes(student_to_switch, worst_day)

        # if there are no good classes to switch, stop
        if class_to_switch == None:
            return

        # check the type of class
        if class_to_switch[0] == 't':
            course_rooms, course_group_dict, course_max_std, student_to_switch_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch, t=True,)
        else:
            course_rooms, course_group_dict, course_max_std, student_to_switch_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch, t=False,)

        # cannot switch if there are no or one classes of particular type
        if course_rooms < 2:
            return

        # pick a new group
        new_group = self.__pick_group(course, course_group_dict, student_to_switch_group)

        # check if there is room, given the type of the class
        if course_group_dict[new_group] < course_max_std:
            course_group_dict[new_group] += 1
            course_group_dict[student_to_switch_group[course.name]] -= 1
            student_to_switch_group[course.name] = new_group

            # compute new malus for the student
            student_to_switch.compute_malus(self.Roster.schedule)
            
            # find the student object to replace with the same student that has new timeslot
            student = self.__find_student_with_id(student_to_switch.id)
            student = student_to_switch

        else:

            #  if full, swap with the worst student in the group
            if class_to_switch[0] == 't':
                students_in_group = [student for student in course.enrolled_students if student.tut_group[course.name] == new_group]
            else:
                students_in_group = [student for student in course.enrolled_students if student.pract_group[course.name] == new_group]
            student_to_switch_new_group = max(students_in_group, key=lambda x: x.malus_count)

            # set variables for new student
            if class_to_switch[0] == 't':
                course_rooms, course_group_dict, course_max_std, student_new_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch_new_group, t=True)
            else:
                course_rooms, course_group_dict, course_max_std, student_new_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch_new_group, t=False)

            # swap students
            student_new_group[course.name] = student_to_switch_group[course.name]
            student_to_switch_group[course.name] = new_group

            # make new timeslots for the students
            student_to_switch_new_group.student_timeslots(self.Roster.schedule)
            student_to_switch.student_timeslots(self.Roster.schedule)  

            # compute new malus for the student
            student_to_switch.compute_malus(self.Roster.schedule)
            student_to_switch_new_group.compute_malus(self.Roster.schedule)

            # compute new malus for the student
            student_to_switch.compute_malus(self.Roster.schedule)
            
            # find the student object to replace with the same student that has new timeslot
            student = self.__find_student_with_id(student_to_switch.id)
            student = student_to_switch

            student = self.__find_student_with_id(student_to_switch_new_group.id)
            student = student_to_switch_new_group

    def __create_student_id_dict(self):
        '''create a dict with students.id as keys so students can be hashed when id is known'''
        self.student_dict = {student.id: student for student in self.student_list}

    def __create_course_name_dict(self):
        '''create a dict with course.name as keys so courses can be hashed when name is known'''
        self.course_dict = {course.name: course for course in self.course_list}

    def __find_course_with_name(self, name):
        '''return course object given its name'''
        return self.course_dict.get(name)

    def __find_student_with_id(self, id):
        '''return student object given its id'''
        return self.student_dict.get(id)

    def __worst_day(self, student_to_switch):
        '''finds worst day in the schedule of a student'''

        worst_score = 0
        worst_day = None

        # go over the timeslot and find day with most gap hour
        for day in student_to_switch.malus_cause['Classes Gap']:
            if student_to_switch.malus_cause['Classes Gap'][day] > worst_score:
                worst_day = day
        if worst_day == None:

            # when worst_day is None, the main method will stop because no classes later on can be found
            return 
        return worst_day

    def __find_classes(self, student_to_switch, worst_day):
        '''picks the class that a student has on his/hers day with most malus points'''

        classes = []
        courses = []
        for course in student_to_switch.timeslots:
            for class_moment in student_to_switch.timeslots[course]:

                if student_to_switch.timeslots[course][class_moment]['day'] == worst_day:
                    # check if it is tut or pract, not a lecture
                    if class_moment[0] == 't' or class_moment[0] == 'p':
                        classes.append(class_moment)
                        courses.append(course)
        
        # pick a random class
        if len(classes) == 0:
            return None, None
        class_to_switch = random.choice(classes)
        course = courses[classes.index(class_to_switch)]

        # get the course object
        course = self.__find_course_with_name(course)

        return class_to_switch, course

    def __tut_or_pract_for_bad_timeslot(self, course, student, t=True):
        '''returns variable names for tutorial groups or practical groups'''

        if t:
            return course.tutorial_rooms, course.tut_group_dict, course.max_std, student.tut_group
        else:
            return course.practical_rooms, course.pract_group_dict, course.max_std_practical, student.pract_group

    def __pick_group(self, course, course_group_dict, student_to_switch_group):
        '''picks a group where a student who needs to swap tutorial or practical groups can go to'''

        picked = False
        while not picked:

            # pick a group to switch to
            groups = list(course_group_dict.keys())
            new_group = random.choice(groups)
            if new_group != student_to_switch_group[course.name]:
                picked = True
        return new_group

class Mutate_double_classes(Mutate):
    def __worst_day(self, student_to_switch):
        '''finds worst day in the schedule of a student'''

        worst_score = 0
        worst_day = None

        # go over the timeslot and find day with most gap hour
        for day in student_to_switch.malus_cause['Dubble Classes']:
            if student_to_switch.malus_cause['Dubble Classes'][day] > worst_score:
                worst_day = day
        if worst_day == None:
            
            # when worst_day is None, the main method will stop because no classes later on can be found
            return 
        return worst_day