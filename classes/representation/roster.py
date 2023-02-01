# This class takes in a list of objects called rooms and makes a roster.
# It can also calculate the total amount maluspoints
from data.assign import student_list, course_list, room_list
import random

class Roster():
    """This class creates a roster of courses, rooms, and students with a schedule of courses and room assignments for each day and time slot."""

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
        for room in self.room_list:
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
