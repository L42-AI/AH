import random

class Mutate():
    def __init__(self, course_list, student_list, schedule):
        self.schedule = schedule

        self.course_list = course_list
        self.student_list = student_list

        # Dict with student and course objects with one attribute as value
        # Makes searching them based on that attribute faster
        self.student_dict = {}
        self.__create_student_id_dict()

        self.course_dict = {}
        self.__create_course_name_dict()

    """ INIT """

    def __create_student_id_dict(self):
        '''create a dict with students.id as keys so students can be hashed when id is known'''
        self.student_dict = {student.id: student for student in self.student_list}

    def __create_course_name_dict(self):
        '''create a dict with course.name as keys so courses can be hashed when name is known'''
        self.course_dict = {course.name: course for course in self.course_list}

    """ GET """

    def __get_course_object(self, name):
        '''return course object given its name'''
        return self.course_dict.get(name)

    def __get_student_object(self, id):
        '''return student object given its id'''
        return self.student_dict.get(id)


    """ METHODS """

    """ Helpers """

    def __find_random_student(self):
        """ This function returns a random student picked from the schedule key called students
            it uses the id it gets from a random course and random class to find the student object 
            with the helper function self.__get_student_object"""

        # get random course, moment and id
        _course = random.choice(list(self.schedule.keys()))
        _class = random.choice(list(self.schedule[_course].keys()))
        student_id = random.choice(list(self.schedule[_course][_class]['students']))

        # # get the object and return it
        # student = self.__get_student_object(student_id)
        return student_id

    def __students_to_shuffle(self):
        """ This function shuffles two random students """

        # Set arbitrary values to enter while loop
        course_picked = False
        student1 = 'a'
        student2 = 'a'

        # While students are not equal and course is not picked
        while student1 == student2 or course_picked == False:

            # Reset course picked boolean
            course_picked = False

            # Randomly select students
            student1 = self.__find_random_student()
            student2 = self.__find_random_student()

            # Find the courses that both students follow
            intersecting_courses = list(set(student1.courses) & set(student2.courses))

            # Skip if no common courses are found
            if len(intersecting_courses) == 0:
                continue

            # Randomly select a course from possible courses
            course = random.choice(intersecting_courses)

            if course.tutorials + course.practicals > 0:
                course_picked = True

        # When different students found:
        self.__shuffle(course, student1, student2)
        return

    def __shuffle(self, course, s1, s2):
        """ This function shuffles two students classes """

        switched = False
        tut_same = False
        pract_same = False
        while switched == False:

            # take a random class types to change
            if course.tutorials == 0:
                class_type = 'practical'

                if pract_same == True:
                    switched = True
            elif course.practicals == 0:
                class_type = 'tutorial'

                if tut_same == True:
                    switched = True
            else:
                class_type = random.choice(['tutorial', 'practical'])

                if tut_same and pract_same == True:
                    switched = True

            if class_type == 'tutorial':
                if s1.tut_group[course.name] == s2.tut_group[course.name]:
                    tut_same = True
                    continue
                else:
                    s1_group = s1.tut_group[course.name]
                    s2_group = s2.tut_group[course.name]

                    s1.tut_group[course.name] = s2_group
                    s2.tut_group[course.name] = s1_group

            elif class_type == 'practical':
                if s1.pract_group[course.name] == s2.pract_group[course.name]:
                    pract_same = True
                    continue
                else:
                    s1_group = s1.pract_group[course.name]
                    s2_group = s2.pract_group[course.name]
                    s1.pract_group[course.name] = s2_group
                    s2.pract_group[course.name] = s1_group

            switched = True


    """ Method 1 """

    def swap_2_students(self):

        self.__students_to_shuffle()

    """ Method 2 """

    def swap_random_lessons(self, empty):

        # check if you want to swap with an empty room or not
        if empty:
            # get one random course and all the empty room time slots
            random_course_1 = random.choice(self.course_list)
            all_lessons_random_2 = [key for key in self.schedule['No course'].keys()]
            course_two = 'No course'

        else:
            # get two random courses
            random_course_1, random_course_2 = random.sample(self.course_list, 2)
            all_lessons_random_2 = list(self.schedule[random_course_2.name].keys())
            course_two = random_course_2.name

        # get all the lessons in that course
        all_lessons_random_1 = list(self.schedule[random_course_1.name].keys())

        # choose two random lessons
        lesson_1 = random.choice(all_lessons_random_1)
        lesson_2 = random.choice(all_lessons_random_2)

        # define in order to be easier to read and to be able to switch keys and values of the dict
        dict_1 = self.schedule[random_course_1.name][lesson_1]
        dict_2 = self.schedule[course_two][lesson_2]

        # switch the times in the schedule roster
        self.schedule[random_course_1.name][lesson_1] = dict(zip(dict_1, dict_2.values()))
        self.schedule[course_two][lesson_2] = dict(zip(dict_2, dict_1.values()))

    """ Helpers """

    def __worst_day(self, id):
        '''finds worst day in the schedule of a student'''

        worst_day = None
        scores_per_day_gap = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0}
        scores_per_day_double = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0}

        student_days, student_classes = self.__fill_timeslots_student(id)

        # For each week
        for day in student_days:

            # Sort timeslots in each day
            timeslot_list = sorted(student_days[day], reverse=True)

            # Only compute if list includes more than 1 timeslot
            if len(timeslot_list) > 1:

                # For each timeslot number: (range is -1 to ensure the use of index + 1)
                for timeslot_num in range(len(timeslot_list) - 1):


                    if timeslot_list[timeslot_num] == timeslot_list[timeslot_num + 1]:
                        scores_per_day_double[day] += 1

                    # claculate the amount of gaps between lessons
                    if timeslot_list[timeslot_num] - timeslot_list[timeslot_num + 1] != 0:
                        lesson_gaps = int((timeslot_list[timeslot_num] - (timeslot_list[timeslot_num + 1] + 2)) / 2)

                        ## update this with global variables!! ##

                        # check if one gap hour
                        if lesson_gaps == 1:
                            scores_per_day_gap[day] += 1

                        elif lesson_gaps == 2:
                            scores_per_day_gap[day] += 3

                        elif lesson_gaps > 2:
                            scores_per_day_gap[day] += 5

        # gets the day with most gap or double hours
        worst_day, gap = self.__get_day_gap_or_double(scores_per_day_double, scores_per_day_gap)

        # if it is zero, zet worst_day to None
        if gap:
            worst_day = self.__return_none(scores_per_day_gap, worst_day)
        else: 
            worst_day = self.__return_none(scores_per_day_double, worst_day)
        
        return worst_day

    def __fill_timeslots_student(self, id):
        student_days = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        student_classes = {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}}
        # go over the schedule and find what timeslots this student has
        for _course in self.schedule:
            for _class in self.schedule[_course]:
                if id in self.schedule[_course][_class]['students']:
                    timeslot = self.schedule[_course][_class]['timeslot']
                    day = self.schedule[_course][_class]['day']
                    group = _class
                    # append the timeslot to the day that class is being held
                    student_days[day].append(timeslot)
                    student_classes[day][_course] = _class
        
        
        return student_days, student_classes



    def __get_day_gap_or_double(self, scores_per_day_double, scores_per_day_gap):
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        gap = True
        return max(scores_per_day_gap, key=lambda x: scores_per_day_gap.get(x)), gap

    def __return_none(self, scores_per_day_gap, worst_day):
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        if scores_per_day_gap[worst_day] == 0:
            worst_day = None
        return worst_day

    def __find_classes(self, student_to_switch, worst_day):
        '''picks the class that a student has on his/hers day with most malus points'''

        courses_per_day = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}

        # go over the schedule and find what timeslots this student has
        for _course in self.schedule:
            for _class in self.schedule[_course]:
                if student_to_switch in self.schedule[_course][_class]['students']:
                    day = self.schedule[_course][_class]['day']

                    # append the timeslot to the day that class is being held
                    courses_per_day[day].append(_course)
                    courses_per_day[day].append(self.schedule[_course].keys())
        
        return courses_per_day

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

    """ Method 3 """

    def swap_bad_timeslots(self):
        '''picks a random student from the student list, finds the day that causes the most gap hours
           and swithces one class from that student.'''

        # pick a student to switch
        student_to_switch = self.__find_random_student()

        # find its worst day
        worst_day = self.__worst_day(student_to_switch)

        # if worst_day had no bad scores, it is none and loop should stop
        if worst_day == None:
            return

        # find student schedule
        student_days, student_classes = self.__fill_timeslots_student(student_to_switch)

        # find a class on its worst day:
        classes_worst_day = None
        for day in student_classes:
            if day == worst_day:
                classes_worst_day = student_classes[day]

        # check if there are non lectures, if there are only lectures, student cannot swap away
        groups = False
        for _class in classes_worst_day:
            if str(classes_worst_day[_class])[0] == 't' or str(classes_worst_day[_class])[0] == 'p':
                groups = True
        if not groups:
            return

        # pick a group that student will switch out of
        tutorial = None
        picked = False
        while not picked:

            # the class that student will be switched inside of and the group student belonged in
            class_to_switch = random.choice(list(classes_worst_day.keys()))
            group = classes_worst_day[class_to_switch]
            if group[0] == 't':
                tutorial = True 
                picked = True
            elif group[0] == 'p':
                tutorial = False
                picked = True

        # switch student
        if tutorial:

            # pick a random tutorial group from that course
            group_found = False
            i = 0
            while not group_found:

                # pick a random group and check if it is of correct type
                new_group = random.choice(list(self.schedule[class_to_switch].keys()))
                if str(new_group)[0] == 't' and new_group != group:
                    group_found = True
                
                # if there is no other group, stop
                i += 1
                if i == 20:
                    return
        
        elif not tutorial:

            # pick a random tutorial group from that course
            group_found = False
            i = 0
            while not group_found:

                # pick a random group and check if it is of correct type
                new_group = random.choice(list(self.schedule[class_to_switch].keys()))
                if str(new_group)[0] == 'p' and new_group != group:
                    group_found = True

                # if there is no other group, stop
                if i == 20:
                    return

        # check if there is room in the new group
        

        raise


        # # check the type of class
        # if group[:8] == 'tutorial':
        #     course_rooms, course_group_dict, course_max_std, student_to_switch_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch, t=True)
        # else:
        #     course_rooms, course_group_dict, course_max_std, student_to_switch_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch, t=False)

        # # cannot switch if there are no or one classes of particular type
        # if course_rooms <= 1:
        #     return

        # # pick a new group
        # new_group = self.__pick_group(course, course_group_dict, student_to_switch_group)

        # # check if there is room, given the type of the class
        # if course_group_dict[new_group] < course_max_std:
        #     course_group_dict[new_group] += 1
        #     course_group_dict[student_to_switch_group[course.name]] -= 1
        #     student_to_switch_group[course.name] = new_group

        #     # compute new malus for the student
        #     student_to_switch.compute_malus(self.schedule)

        #     # find the student object to replace with the same student that has new timeslot
        #     student = self.__get_student_object(student_to_switch.id)
        #     student = student_to_switch
        # else:

        #     #  if full, swap with the worst student in the group
        #     if class_to_switch[:8] == 'tutorial':
        #         students_in_group = [student for student in course.enrolled_students if student.tut_group[course.name] == new_group]
        #     else:
        #         students_in_group = [student for student in course.enrolled_students if student.pract_group[course.name] == new_group]

        #     # Find student to switch based on the highest malus
        #     student_to_switch_new_group = max(students_in_group, key=lambda x: x.malus_count)

        #     # set variables for new student
        #     if class_to_switch[:8] == 'tutorial':
        #         course_rooms, course_group_dict, course_max_std, student_new_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch_new_group, t=True)
        #     else:
        #         course_rooms, course_group_dict, course_max_std, student_new_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch_new_group, t=False)

        #     # swap students
        #     student_new_group[course.name] = student_to_switch_group[course.name]
        #     student_to_switch_group[course.name] = new_group

        #     # make new timeslots for the students
        #     student_to_switch_new_group.student_timeslots(self.schedule)
        #     student_to_switch.student_timeslots(self.schedule)

        #     # compute new malus for the student
        #     student_to_switch.compute_malus(self.schedule)
        #     student_to_switch_new_group.compute_malus(self.schedule)

        #     # compute new malus for the student
        #     student_to_switch.compute_malus(self.schedule)

        #     # find the student object to replace with the same student that has new timeslot
        #     student = self.__get_student_object(student_to_switch.id)
        #     student = student_to_switch

        #     student = self.__get_student_object(student_to_switch_new_group.id)
        #     student = student_to_switch_new_group


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
            return None
        return worst_day

class Mutate_Course_Swap_Capacity(Mutate):
    def _get_course(self, empty):
        if empty:
            random_course_1 = self.Roster.course_capacity_malus_sorted[0]
            random_course_2 = None
        else:
            # get two random courses
            random_course_1 = self.Roster.course_capacity_malus_sorted[0]
            picked = False
            while not picked:
                random_course_2 = random.choice(self.course_list)
                if random_course_2.name != random_course_1.name:
                    picked = True
        return random_course_1, random_course_2