# This class takes in a list of objects called rooms and makes a roster.
# It can also calculate the total amount maluspoints
import random

class Roster():
    """This class creates a roster of courses, rooms and students with a schedule of courses and room assignments for each day and timeslot."""

    def __init__(self, rooms_list, student_list, course_list, capacity=False):
        self.schedule = {}
        self.rooms_list = rooms_list
        self.student_list = student_list
        self.course_list = course_list
        self.course_capacity_malus_sorted = []

        # this is a greedy function with as default set to False
        self.CAPACITY = capacity

    def init_student_timeslots(self, student_list):
        """This method takes in a list of students and initializes student timeslots for all students in the roster."""

        # loop over each student and initialize the timeslots
        for student in student_list:
            student.student_timeslots(self)

    def __merge(self, dict1, dict2):
        """This method takes in two dictionaries and returns the merged dictionary."""
        return{**dict1, **dict2}

    def __init_malus(self):
        """This method initialized the malus counters for all the different causes."""
        
        self.malus_count = 0
        self.malus_cause = {}
        self.malus_cause['Night'] = 0
        self.malus_cause['Capacity'] = 0

        # you can call this somewhere apart so that it doesnt get merged every single iteration of total malus,
        # then set everything to 0
        student_malus_cause = {'Classes Gap': 0, 'Double Classes': 0, 'Tripple Gap': 0}
        self.malus_cause = self.__merge(self.malus_cause, student_malus_cause)

    def total_malus(self, student_list):
        """This function loops over the list filled with Student objects and calculates the total maluspoints"""

        self.__init_malus()

        self.check_malus()

        # For each student
        for student in student_list:

            # Compute the malus
            student.malus_points(self)

            # Add to complete malus counter
            self.malus_count += student.malus_count

            # Add to complete malus counter
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            for day in days:

                self.malus_cause['Tripple Gap'] += student.malus_cause['Tripple Gap'][day]
                self.malus_cause['Classes Gap'] += student.malus_cause['Classes Gap'][day]
                self.malus_cause['Double Classes'] += student.malus_cause['Double Classes'][day]

    def __place_in_schedule(self, room, day, timeslot, course_name, classes, max_std):
        # if classes[0] != 'l' and course_name != 'No course':
            # print(max_std)
        # only need class if it is an actual lesson
        self.schedule[course_name][classes] = {}
        self.schedule[course_name][classes]['day'] = day
        self.schedule[course_name][classes]['timeslot'] = timeslot
        self.schedule[course_name][classes]['room'] = room.id
        self.schedule[course_name][classes]['capacity'] = room.capacity
        self.schedule[course_name][classes]['max students'] = max_std
        self.schedule[course_name][classes]['students'] = set()

        room.availability[day][timeslot] = False

    def fill_empty_slots(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # Set possible timeslots
        timeslots = [9, 11, 13, 15]
        self.schedule["No course"] = {}
        i = 1

        # check every room if they are being used at every moment
        for room in self.rooms_list:
            for day in days:
                for timeslot in timeslots:
                    if room.availability[day][timeslot]:
                        classes = f"No classes {i}"

                        # schedule the room as empty
                        self.__place_in_schedule(room, day, timeslot, "No course", classes, 1000)
                        i += 1
                if room.id == 'C0.110':
                    if room.availability[day][17]:
                        classes = f"No classes {i}"
                        self.__place_in_schedule(room, day, 17, "No course", classes, 1000)
                        i += 1

    def fill_schedule_random(self, course, class_type, count, attending):
        """ This function fills a schedule with no student restraints. If there are no rooms available it prints an Error message."""

        # Make key if not existent
        if course.name not in self.schedule:
            self.schedule[course.name] = {}

        i = 0
        succes = False
        while not succes:
            i += 1
            # Generate a random room, day and timeslot:
            room = random.choice(self.rooms_list)
            day = random.choice(list(room.availability.keys()))
            timeslot = random.choice(list(room.availability[day].keys()))

            # If timeslot is available
            if room.availability[day][timeslot]:

                # first try with specific room for the type of class
                if self.CAPACITY:
                    if i < 20:
                        if class_type == 'lecture' and room.id == 'A1.08' or room.id == 'A1.06':
                            continue
                        if class_type != 'lecture' and room.id == 'C0.110' or room.id == 'C0.112':
                            continue
                if course.lecture_day != None:
                    if course.lecture_day != day and class_type == 'lecture':
                        continue

                self.schedule[course.name][f'{class_type} {count}'] = {}
                class_number = f"{class_type} {count}"
                
                if class_number[0] == 't':
                    self.__place_in_schedule(room, day, timeslot, course.name, class_number, course.max_std)
                    # print(f'tut: {course.max_std}')
                elif class_number[0] == 'p':
                    self.__place_in_schedule(room, day, timeslot, course.name, class_number, course.max_std_practical)
                    # print(f'pract: {course.max_std_practical}')
                else:
                    self.__place_in_schedule(room, day, timeslot, course.name, class_number, 1000)
                    

                succes = True

    def check_malus(self):
        """
        This function checks if a course group is in the late timeslot and 
        whether the amount of attending students is higher then the capacity of that room.
        It then increases the maluspoints respectively.
        """

        # For each course:
        for course in self.course_list:

            # Find all classes
            for classes in self.schedule[course.name]:

                # Set the number of class
                class_number = int(classes[-1])

                # Set attending amount of correct class type
                if classes.startswith('tut'):
                    attending = course.tut_group_dict[class_number]
                elif classes.startswith('prac'):
                    attending = course.pract_group_dict[class_number]
                else:
                    attending = course.enrolled

                # Set timeslot of class
                timeslot = self.schedule[course.name][classes]['timeslot']

                # For each room:
                for room in self.rooms_list:

                    # If room id is room id of class
                    if self.schedule[course.name][classes]['room'] == room.id:

                        # Set capacity
                        capacity = room.capacity

                # Penalty for late night lesson
                if timeslot == 17:
                    self.malus_cause['Night'] += 5
                    self.malus_count += 5

                # Penalty for overrun capacity
                occupation = attending - capacity
                if occupation > 0:
                    self.malus_cause['Capacity'] += occupation
                    self.malus_count += occupation

                    # store inside the course how many occupation malus it caused
                    course.capacity_malus += occupation

        self.course_capacity_malus_sorted = sorted(self.course_list, key=lambda x: x.capacity_malus)