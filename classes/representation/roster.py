# This class takes in a list of objects called rooms and makes a roster.
# It can also calculate the total amount maluspoints
from data.assign import student_list, course_list, room_list
import random

class Roster():
    """
    This class creates a roster of courses, rooms, and students with
    a schedule of courses and room assignments for each day and time slot.
    """

    def __init__(self, capacity=False):
        self.schedule = {}
        self.room_list = room_list
        self.student_list = student_list
        self.course_list = course_list
        self.course_capacity_malus_sorted = []

        # capacity is a greedy function with default False
        self.CAPACITY = capacity

    def init_student_timeslots(self):
        """This method takes in a student list and initializes student time slots for all the students."""

        # loop over the list of students and initialize timeslots
        for student in self.student_list:
            student.student_timeslots(self)

    def __place_in_schedule(self, room, day, timeslot, course_name, classes, max_std):
        """ This method places a dictionary into the right class with all the necessary information """

        # set all the necessary information into the dictionary for the right class key
        self.schedule[course_name][classes] = {}
        self.schedule[course_name][classes]['day'] = day
        self.schedule[course_name][classes]['timeslot'] = timeslot
        self.schedule[course_name][classes]['room'] = room.id
        self.schedule[course_name][classes]['capacity'] = room.capacity
        self.schedule[course_name][classes]['max students'] = max_std
        self.schedule[course_name][classes]['students'] = set()

        # set the room availability to False in order to negate double rostering of rooms
        room.availability[day][timeslot] = False

    def fill_empty_slots(self):
        """ 
        This method makes a new key in the schedule and as value fills all the rooms and their timeslots,
        that have not been scheduled yet.
        """

        # Set possible timeslots and days
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        timeslots = [9, 11, 13, 15]

        # count the empty seminar moments
        i = 0

        # add new key to the schedule
        self.schedule["No course"] = {}

        # check every room if they are being used at every moment
        for room in self.room_list:

            # if the room is C0.110 check the late timeslot as well
            if room.id == 'CO.110':
                timeslots = [9, 11, 13, 15, 17]

            for day in days:
                for timeslot in timeslots:
                    if room.availability[day][timeslot]:
                        classes = f"No classes {i}"

                        # schedule the room as empty
                        self.__place_in_schedule(room, day, timeslot, "No course", classes, 1000)

                        i += 1

                # # if the room is C0.110 check the late timeslot as well
                # if room.id == 'C0.110':
                #     if room.availability[day][17]:
                #         classes = f"No classes {i}"
                #         self.__place_in_schedule(room, day, 17, "No course", classes, 1000)

    def fill_schedule_random(self, course, class_type, count):
        """ This function fills a schedule with no student capacity restraints in a random fassion """

        # Make key if not existent
        if course.name not in self.schedule:
            self.schedule[course.name] = {}

        # counter
        i = 0

        succes = False
        while not succes:

            # count plus 1
            i += 1

            # Generate a random room, day and timeslot:
            room = random.choice(self.room_list)
            day = random.choice(list(room.availability.keys()))
            timeslot = random.choice(list(room.availability[day].keys()))

            # If timeslot is available
            if room.availability[day][timeslot]:

                # first try with specific room for the type of class / part of the greedy algorithm
                if self.CAPACITY:
                    if i < 20:
                        if class_type == 'lecture' and room.id == 'A1.08' or room.id == 'A1.06':
                            continue
                        if class_type != 'lecture' and room.id == 'C0.110' or room.id == 'C0.112':
                            continue
                
                # check if the lecture_day is None if not check if its a lecture, if it is skip the rostering
                # part of the most POPULAR and DIFICULT_STUDENTS algorithm in generator.py
                if course.lecture_day != None:
                    if course.lecture_day != day and class_type == 'lecture':
                        continue

                self.schedule[course.name][f'{class_type} {count}'] = {}
                class_number = f"{class_type} {count}"

                # if the class is a tutorial roster it
                if class_number[0] == 't':
                    self.__place_in_schedule(room, day, timeslot, course.name, class_number, course.max_std_tutorial)\

                # if the class is a practical roster it
                elif class_number[0] == 'p':
                    self.__place_in_schedule(room, day, timeslot, course.name, class_number, course.max_std_practical)

                # roster the lecture
                else:
                    self.__place_in_schedule(room, day, timeslot, course.name, class_number, 1000)

                succes = True
            i += 1
