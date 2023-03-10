import copy
from data.assign import student_list, course_list, room_list

class MC:
    """
    Class that handles malus calculations. It uses the schedule and the set of
    students connnected to each seminar to do so
    """

    def __init__(self) -> None:

        # Set lists
        self.course_list = course_list
        self.student_list = student_list
        self.room_list = room_list

        # Init dictionaries for hashable refernce
        self.init_student_dict()
        self.init_course_dict()

    """ INIT """

    def init_malus(self) -> None:
        '''
        create a malus dictionary that will hold the points
        '''

        self.malus = {}

        # Set all malus cause counts
        self.malus['Total'] = 0
        self.malus['Night'] = 0
        self.malus['Capacity'] = 0
        self.malus['Double Classes'] = 0
        self.malus['Classes Gap'] = 0
        self.malus['Triple Gap'] = 0

    def init_student_dict(self) -> None:
        """
        Create a student dict that links ids to object
        """

        self.student_dict = {}

        # For each student object
        for student in self.student_list:
            self.student_dict[student.id] = student

    def init_course_dict(self) -> None:
        """
        Create a course dict that links ids to object
        """

        self.course_dict= {}

        # For each course object
        for course in self.course_list:
            self.course_dict[course.name] = course

    """ GET """

    def get_student(self, id) -> object:
        '''
        returns student object
        '''
        return self.student_dict.get(id)

    def get_course(self, name) -> object:
        '''
        returns course object
        '''
        return self.course_dict.get(name)

    """ Methods """

    def compute_schedule_malus(self, schedule) -> None:
        '''
        computes the malus by looping over every course and its seminars
        in the schedule
        '''

        # For each course:
        for course_name in schedule:

            # Skip if course is None
            if course_name == 'No course':
                continue

            # Get course object from dict
            course_obj = self.get_course(course_name)

            # For each class
            for class_moment in schedule[course_name]:

                # Set the number of class
                class_number = int(class_moment[-1])

                # Set attending amount of correct class type
                if class_moment.startswith('tut'):
                    attending = copy.copy(course_obj.tut_group_dict[class_number])
                elif class_moment.startswith('prac'):
                    attending = copy.copy(course_obj.pract_group_dict[class_number])
                else:
                    attending = copy.copy(course_obj.enrolled)

                # Set timeslot of class
                timeslot = copy.copy(schedule[course_name][class_moment]['timeslot'])

                # For each room:
                for room in self.room_list:

                    # If room id is room id of class
                    if schedule[course_name][class_moment]['room'] == room.id:

                        # Set capacity
                        capacity = copy.copy(room.capacity)

                # Penalty for late night lesson
                if timeslot == 17:
                    self.malus['Night'] += 5
                    self.malus['Total'] += 5

                # Penalty for overrun capacity
                occupation = attending - capacity
                if occupation > 0:
                    self.malus['Capacity'] += occupation
                    self.malus['Total'] += occupation

    def __days_in_schedule(self, schedule) -> dict:
        '''
        returns a dictionary called timeslots that holds the information about gap and double hours
        for every student
        '''

        # Create empty dict
        timeslots = {}

        # For each course
        for course in schedule:

            # For each class
            for class_moment in schedule[course]:

                # For each student in class
                for student_id in schedule[course][class_moment]['students']:

                    # Create if timeslot non existent
                    if student_id not in timeslots:
                        timeslots[student_id] = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}

                    # Fill with information about timeslot
                    timeslots[student_id][schedule[course][class_moment]['day']].append(schedule[course][class_moment]['timeslot'])

        return timeslots

    def compute_student_malus(self, schedule) -> None:
        '''
        Uses the timeslots dictionary to go over every student in order to
        'reward' the malus points associated with his/hers schedule
        '''

        # Set timeslots
        timeslots = self.__days_in_schedule(schedule)

        # For each student
        for student_id in timeslots:

            # For each week
            for day in timeslots[student_id]:

                # Sort timeslots in each day
                timeslot_list = sorted(timeslots[student_id][day], reverse=True)

                # Only compute if list includes more than 1 timeslot
                if len(timeslot_list) > 1:

                    # keep track if students have double classes that day
                    timeslots_double_classes = []

                    # For each timeslot number: (range is -1 to ensure the use of index + 1)
                    for timeslot_num in range(len(timeslot_list) - 1):

                        # malus for double classes
                        if timeslot_list[timeslot_num] in timeslots_double_classes:
                            self.malus['Double Classes'] += 1
                            self.malus['Total'] += 1
                        else:
                            timeslots_double_classes.append(timeslot_list[timeslot_num])

                        # claculate the amount of gaps between lessons
                        if timeslot_list[timeslot_num] - timeslot_list[timeslot_num + 1] != 0:
                            lesson_gaps = int((timeslot_list[timeslot_num] - (timeslot_list[timeslot_num + 1] + 2)) / 2)

                            # check for lesson gaps and attribute malus
                            if lesson_gaps == 1:
                                self.malus['Classes Gap'] += 1
                                self.malus['Total'] += 1

                            elif lesson_gaps == 2:
                                self.malus['Classes Gap'] += 3
                                self.malus['Total'] += 3

                            elif lesson_gaps > 2:
                                self.malus['Triple Gap'] += 5
                                self.malus['Total'] += 5

    def compute_total_malus(self, schedule) -> dict:
        '''
        method to call on outside this class that calls all malus
        calculation methods in the correct order
        '''

        self.init_malus()
        self.compute_schedule_malus(schedule)
        self.compute_student_malus(schedule)
        return self.malus
