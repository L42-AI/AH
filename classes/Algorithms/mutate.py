import random

class Mutate():
    def __init__(self, course_list, student_list, schedule):
        self.schedule = schedule
        self.course_list = course_list
        self.student_list = student_list
<<<<<<< HEAD

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

    


    def __find_random_student(self) -> int:
        """ This function returns a random student picked from the schedule key called students
            it uses the id it gets from a random course and random class to find the student object 
            with the helper function self.__get_student_object"""

        # get random course, moment and id
        _course = random.choice(list(self.schedule.keys()))

        # do not accept the schedule filler
        while _course == 'No course':
            _course = random.choice(list(self.schedule.keys()))

        _class = random.choice(list(self.schedule[_course].keys()))

        _students = list(self.schedule[_course][_class]['students'])
        try:
            student_id = random.choice(_students)
        except:
            print(_class, _students, self.schedule[_course][_class])
            print(self.schedule)
            raise
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
=======
        self.double = {'l': {'v': 0, 'student': []}, 't': {'v': 0, 'student': []}, 'p': {'v': 0, 'student': []}}

    """ Method 1 """
>>>>>>> 89a5c05c8dfca886a002002fb1b03663054a622c

    def swap_2_students(self):

        self.__students_to_shuffle()

    """ Method 2 """

    def swap_random_lessons(self, empty):

        all_lessons_random_1, all_lessons_random_2, random_course_1, random_course_2 =  self.get_two_courses(empty)

        # choose two random lessons
        lesson_1 = random.choice(all_lessons_random_1)
        lesson_2 = random.choice(all_lessons_random_2)

        roomslot1 = self.schedule[random_course_1][lesson_1]
        roomslot2 = self.schedule[random_course_2][lesson_2]

        # first swap students, because when we swap, we want to get the students back to their course
        keys = ['day', 'timeslot', 'capacity', 'room']
        room1_data = {key: roomslot1[key] for key in keys}
        room2_data = {key: roomslot2[key] for key in keys}

        roomslot1.update(room2_data)
        roomslot2.update(room1_data)

    def swap_bad_timeslots(self):
        '''picks a random student from the student list, finds the day that causes the most gap or double hours
           and swithces one class from that student'''

        # pick a student to switch
        student_to_switch_id = self.__find_random_student()
        
        # find its worst day
        worst_day = self.__worst_day(student_to_switch_id)

        # if worst_day had no bad scores, it is none and loop should stop
        if worst_day == None:
            return

        # find student schedule
        _, student_classes = self.__fill_timeslots_student(student_to_switch_id)

        # find a class on its worst day:
        classes_worst_day = student_classes[worst_day]

        # make sure there are other practicals or tutorials to switch with
        if not self.__non_lectures(classes_worst_day):
            return

        switch_in_this_course, new_group, old_group = self.__pick_groups_to_switch(classes_worst_day)
        if switch_in_this_course == None:
            return
        
        new_group = self.schedule[switch_in_this_course][new_group]
        old_group = self.schedule[switch_in_this_course][old_group]

        self.__swap_student_or_students(new_group, old_group, student_to_switch_id)

    '''THESE METHODS ARE HELPER FUNCTIONS TO THE METHODS THAT THE HILLCLIMBERS CALL ON'''
    def get_two_courses(self, empty):
        '''returns two courses, 2nd one will be an empty timeslot if empty=true.
           This method will be adjusted when selecting the first course on capacity malus'''

        # check if you want to swap with an empty room or not
        if empty:
            # get one random course and all the empty room time slots
            random_course_1 = random.choice(self.course_list)
            all_lessons_random_2 = [key for key in self.schedule['No course'].keys()]
            random_course_2 = 'No course'

        else:
            # get two random courses
            random_course_1, random_course_2 = random.sample(self.course_list, 2)
            random_course_2 = random_course_2.name
            all_lessons_random_2 = list(self.schedule[random_course_2].keys())
        
        # get all the lessons in that course
        random_course_1 = random_course_1.name
        all_lessons_random_1 = list(self.schedule[random_course_1].keys())

        return all_lessons_random_1, all_lessons_random_2, random_course_1, random_course_2

    def __find_random_student(self) -> int:
        """ This function returns a random student picked from the schedule key called students
            it uses the id it gets from a random course and random class to find the student object 
            with the helper function self.__get_student_object"""

        # get random course, moment and id
        _course = random.choice(list(self.schedule.keys()))

        # do not accept the schedule filler 
        while _course == 'No course':
            _course = random.choice(list(self.schedule.keys()))

        _class = random.choice(list(self.schedule[_course].keys()))

        _students = list(self.schedule[_course][_class]['students'])
        student_id = random.choice(_students)

        return student_id

    def __non_lectures(self, classes_worst_day):
        '''a student cannot swap with a lecture because he has to be present to all of them
            so this method checks if there are more classes other than lectures and his own so we
            know there is something to switch to'''
        # check if there are non lectures, if there are only lectures, student cannot swap away
        for _class in classes_worst_day:
            if str(classes_worst_day[_class])[:8] == 'tutorial' or str(classes_worst_day[_class])[:9] == 'practical':
                return True
        return False

    def __pick_groups_to_switch(self, classes_worst_day):
        '''gets the classes that a student has on its worst day and picks one he/she will switch out of
           after doing so, it uses self.schedule to find when other tutorials or practicals are held and
           picks one to go to'''

        # pick a group that student will switch out of
        tutorial = None
        picked = False
        while not picked:

            # the class that student will be switched outside of and the group student belonged in
            switch_in_this_course = random.choice(list(classes_worst_day.keys()))
            old_group = classes_worst_day[switch_in_this_course]
            if old_group[:8] == 'tutorial':
                tutorial = True 
                picked = True
            elif old_group[:9] == 'practical':
                tutorial = False
                picked = True

        # switch student
        if tutorial:
            group_type = 't'
        if not tutorial:
            group_type = 'p'

        # pick a random tutorial group from that course
        group_found = False
        i = 0
        while not group_found:

            # pick a random group and check if it is of correct type
            new_group = random.choice(list(self.schedule[switch_in_this_course].keys()))
            if str(new_group)[0] == group_type and new_group != old_group:
                group_found = True
            
            # if there is no other group, stop
            i += 1
            if i == 20:
                return None, None, None
        return switch_in_this_course, new_group, old_group

    def __swap_student_or_students(self, new_group, old_group, student_to_switch_id):
        '''takes a student, a group the student came from and a group the students needs to go and makes it happen
           if the group the student needs to go to is full, it will randomly place one of the students to the original
           group to create space'''

        if len(new_group['students']) < new_group['max students']:
            self.__place_student_in_group(student_to_switch_id, new_group, old_group)
            return
        else:
            # pick a random student to switch with
            student_to_old_group = random.choice(list(new_group['students']))
            self.__place_student_in_group(student_to_switch_id, new_group, old_group)
            self.__place_student_in_group(student_to_old_group, old_group, new_group)
            return

    def __place_student_in_group(self, student_to_switch_id, new_group, old_group):
        '''places a student in the 'student' set that every group has'''
        new_group['students'].add(student_to_switch_id)
        old_group['students'].remove(student_to_switch_id)

    def __worst_day(self, id) -> str:
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
<<<<<<< HEAD
        worst_day = self.__get_day_gap_or_double(scores_per_day_double, scores_per_day_gap)
=======
        worst_day = self.get_day_gap_or_double(scores_per_day)
        worst_day = self.return_none(scores_per_day, worst_day)

        return worst_day
    
    def __worst_day_test_for_double(self, id):
        '''finds worst day in the schedule of a student but keeps track
           of double hours and what caused them, method will mostly be used 
           in testing'''

        worst_day = None
        student_days, student_classes = self.__fill_timeslots_student_test_for_double(id)

        scores_per_day = {day:(0, {'value': 0, 'l': 0, 't': 0, 'p':0}) for day in student_days}

        
        # For each week
        for day in student_days:
            day_dict = {'value': 0, 'l': 0, 't': 0, 'p':0}
            
            # Sort timeslots in each day
            only_time = [x[0] for x in student_days[day]]
            timeslot_list = sorted(only_time, reverse=True)

            # Only compute if list includes more than 1 timeslot
            if len(timeslot_list) > 1:

                # For each timeslot number: (range is -1 to ensure the use of index + 1)
                for timeslot_num in range(len(timeslot_list) - 1):
                    day_dict['value'] += 1

                    if timeslot_list[timeslot_num] == timeslot_list[timeslot_num + 1]:

                        scores_per_day[day] = (scores_per_day[day][0], day_dict)
                        if student_days[day][timeslot_num][1][0] == 'l':
                            day_dict['l'] += 1
                            self.double['l']['v'] += 1
                            self.double['l']['student'].append(id)
                            scores_per_day[day] = (scores_per_day[day][0], scores_per_day[day][1]['l'] + 1)
                        if student_days[day][timeslot_num][1][0] == 't':
                            day_dict['t'] += 1
                            self.double['t']['v'] += 1
                            self.double['t']['student'].append(id)
                        if student_days[day][timeslot_num][1][0] == 'p':
                            day_dict['p'] += 1
                            self.double['p']['v'] += 1
                            self.double['p']['student'].append(id)

                    # claculate the amount of gaps between lessons
                    if timeslot_list[timeslot_num] - timeslot_list[timeslot_num + 1] != 0:
                        lesson_gaps = int((timeslot_list[timeslot_num] - (timeslot_list[timeslot_num + 1] + 2)) / 2)

                        # check if one gap hour
                        if lesson_gaps == 1:
                            scores_per_day[day] = (scores_per_day[day][0] + 1, scores_per_day[day][1])

                        elif lesson_gaps == 2:
                            scores_per_day[day] = (scores_per_day[day][0] + 3, scores_per_day[day][1])

                        elif lesson_gaps > 2:
                            scores_per_day[day] = (scores_per_day[day][0] + 5, scores_per_day[day][1])
                    scores_per_day[day] = (scores_per_day[day][0], day_dict)
        # gets the day with most gap or double hours
        worst_day = self.get_day_gap_or_double_test_for_double(scores_per_day)
>>>>>>> 89a5c05c8dfca886a002002fb1b03663054a622c

        return worst_day

    def __fill_timeslots_student(self, id) -> dict:
        '''fills the timeslot of a student based on the complete schedule 
           days keeps track of the timeslot, classes of the info of that specific class'''
        student_days = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        student_classes = {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}}
        # go over the schedule and find what timeslots this student has
        for _course in self.schedule:
            for _class in self.schedule[_course]:
                if id in self.schedule[_course][_class]['students']:
                    timeslot = self.schedule[_course][_class]['timeslot']
                    day = self.schedule[_course][_class]['day']

                    # append the timeslot to the day that class is being held
                    student_days[day].append(timeslot)
                    student_classes[day][_course] = _class

        return student_days, student_classes

<<<<<<< HEAD


    def __get_day_gap_or_double(self, scores_per_day_double, scores_per_day_gap) -> str:
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        return max(scores_per_day_gap, key=lambda x: scores_per_day_gap.get(x))
=======
    def __fill_timeslots_student_test_for_double(self, id):
        '''fills the timeslot of a student based on the complete schedule
           days keeps track of the timeslot, classes of the info of that specific class
           also keeps track of double hours by appending a tuple to student_days instead of just timeslot'''
        
        student_days = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        student_classes = {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}}

        # go over the schedule and find what timeslots this student has
        for _course in self.schedule:
            for _class in self.schedule[_course]:
                if id in self.schedule[_course][_class]['students']:
                    timeslot = self.schedule[_course][_class]['timeslot']
                    day = self.schedule[_course][_class]['day']

                    # append the timeslot to the day that class is being held
                    student_days[day].append((timeslot, _class))
                    student_classes[day][_course] = _class

        return student_days, student_classes


    def get_day_gap_or_double(self, scores_per_day):
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        
        return max(scores_per_day, key=lambda x: x[0])

    def get_day_gap_or_double_test_for_double(self, scores_per_day):
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''

        best_score = 0
        worst_day = None
        for key in scores_per_day:
  
            score = scores_per_day[key][0]
            if score >= best_score:
                best_score = score
                worst_day = key

        return worst_day
>>>>>>> 89a5c05c8dfca886a002002fb1b03663054a622c

    def return_none(self,scores_per_day, worst_day):
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        if scores_per_day[worst_day][0] == 0:
            worst_day = None
        return worst_day

<<<<<<< HEAD
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

        GAP = self.__gap()

        # pick a student to switch
        student_to_switch_id = self.__find_random_student()

        # find its worst day
        worst_day = self.__worst_day(student_to_switch_id)

        # if worst_day had no bad scores, it is none and loop should stop
        if worst_day == None:
            return

        # find student schedule
        _, student_classes = self.__fill_timeslots_student(student_to_switch_id)

        # find a class on its worst day:
        classes_worst_day = student_classes[worst_day]

        # check if there are non lectures, if there are only lectures, student cannot swap away
        groups = False
        for _class in classes_worst_day:
            if str(classes_worst_day[_class])[:8] == 'tutorial' or str(classes_worst_day[_class])[:9] == 'practical':
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
            if group[:8] == 'tutorial':
                tutorial = True 
                picked = True
            elif group[:9] == 'practical':
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

            # pick a random tutorial group from that cours
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
        new_group = self.schedule[class_to_switch][new_group]
        if len(new_group['students']) < new_group['max students']:

            new_group['students'].add(student_to_switch_id)
            self.schedule[class_to_switch][group]['students'].remove(student_to_switch_id)
            return
        else:
            # pick a random student to switch with
            student_to_old_group = random.choice(list(new_group['students']))
            new_group['students'].add(student_to_switch_id)
            new_group['students'].remove(student_to_old_group)
            self.schedule[class_to_switch][group]['students'].remove(student_to_switch_id)
            self.schedule[class_to_switch][group]['students'].add(student_to_old_group)
            return

    def __gap(self):
        return False

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


=======
>>>>>>> 89a5c05c8dfca886a002002fb1b03663054a622c
class Mutate_double_classes(Mutate):
    '''mutate class that is the same as normal but makes changes to 
       the schedule based on the malus points caused by double hours instead
       of the gap hour points'''

<<<<<<< HEAD
    def __get_day_gap_or_double(self, scores_per_day_double, scores_per_day_gap):
        print('WORKING')
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        return max(scores_per_day_double, key=lambda x: scores_per_day_double.get(x))
=======
    def get_day_gap_or_double(self, scores_per_day):
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        return max(scores_per_day, key=lambda x: x[1])

    def get_day_gap_or_double_test_for_double(self, scores_per_day):
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        # print(scores_per_day)
        best_score = 0
        for key in scores_per_day:
            print(f'key: {key}')
            score = scores_per_day[key][1]['value']
            if score >= best_score:
                best_score = score
                worst_day = key

        return key
>>>>>>> 89a5c05c8dfca886a002002fb1b03663054a622c

    def return_none(self,scores_per_day, worst_day):
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        if scores_per_day[worst_day][1] == 0:
            worst_day = None
        return worst_day

class Mutate_Course_Swap_Capacity(Mutate):
    '''same as the normal mutate, but instead of switching
       lectures or tutorials randomly, it checks what lecture or tutorial
       causes the most capacity trouble'''
       
    def get_two_courses(self, empty):
        # check if you want to swap with an empty room or not
        self.course_list.sort(key=lambda x: x.capacity_malus, reverse=True)
        course_1 = self.course_list[0]

        if empty:
            # get one random course and all the empty room time slots
            all_lessons_random_2 = [key for key in self.schedule['No course'].keys()]
            random_course_2 = 'No course'

        else:
            # first exclude course one from the course list
            course_list = [course.name for course in self.course_list if course != course_1]

            # pick a random second course
            random_course_2 = random.sample(course_list, 1)[0]
            
            # find all the lessons associated with it
            all_lessons_random_2 = list(self.schedule[random_course_2].keys())
        
        # get all the lessons from course 1
        course_1 = course_1.name
        all_lessons_random_1 = list(self.schedule[course_1].keys())

        return all_lessons_random_1, all_lessons_random_2, course_1, random_course_2