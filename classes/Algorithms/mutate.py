import random

class Mutate():
    def __init__(self, course_list, student_list, schedule):
        self.schedule = schedule
        self.course_list = course_list
        self.student_list = student_list
        self.double = {'l': {'v': 0, 'student': []}, 't': {'v': 0, 'student': []}, 'p': {'v': 0, 'student': []}}

    """ Method 1 """

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
        _, student_classes = self._fill_timeslots_student(student_to_switch_id)

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
        student_days, student_classes = self.__fill_timeslots_student(id)

        scores_per_day = {day:(0, 0) for day in student_days}
        
        # For each week
        for day in student_days:

            # Sort timeslots in each day
            timeslot_list = sorted(student_days[day], reverse=True)

            # Only compute if list includes more than 1 timeslot
            if len(timeslot_list) > 1:

                # For each timeslot number: (range is -1 to ensure the use of index + 1)
                for timeslot_num in range(len(timeslot_list) - 1):


                    if timeslot_list[timeslot_num] == timeslot_list[timeslot_num + 1]:
                        scores_per_day[day] = (scores_per_day[day][0], scores_per_day[day][1] + 1)

                    # claculate the amount of gaps between lessons
                    if timeslot_list[timeslot_num] - timeslot_list[timeslot_num + 1] != 0:
                        lesson_gaps = int((timeslot_list[timeslot_num] - (timeslot_list[timeslot_num + 1] + 2)) / 2)

                        ## update this with global variables!! ##

                        # check if one gap hour
                        if lesson_gaps == 1:
                            scores_per_day[day] = (scores_per_day[day][0] + 1, scores_per_day[day][1])

                        elif lesson_gaps == 2:
                            scores_per_day[day] = (scores_per_day[day][0] + 3, scores_per_day[day][1])

                        elif lesson_gaps > 2:
                            scores_per_day[day] = (scores_per_day[day][0] + 5, scores_per_day[day][1])

        # gets the day with most gap or double hours
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

        return worst_day

    def _fill_timeslots_student(self, id) -> dict:
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

    def return_none(self,scores_per_day, worst_day):
        '''EDIT THIS IN THE DOUBLE HOUR CLASS'''
        if scores_per_day[worst_day][0] == 0:
            worst_day = None
        return worst_day

class Mutate_double_classes(Mutate):
    '''mutate class that is the same as normal but makes changes to
       the schedule based on the malus points caused by double hours instead
       of the gap hour points'''

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