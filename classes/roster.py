# This class takes in a list of objects called rooms and makes a roster.
# It can also calculate the total amount maluspoints
import functions.schedule_fill as schedule_fill
import functions.helpers as help_function
import random

class Roster():
    def __init__(self, rooms):
        self.schedule = {}
        self.rooms = rooms

        self.malus_count = 0

        self.lecture_fill_preference = -10
        self.class_fill_preference = -5

        self.malus_cause = {}
        self.init_malus()

        # shuffle the list of room object for the random initialze
        random.shuffle(self.rooms)

    def init_malus(self):
        self.malus_cause['Night'] = 0
        self.malus_cause['Capacity'] = 0


    def total_malus(self, student_list):
        """This function loops over the list filled with Student objects and calculates the total maluspoints"""
        student_malus_cause = {'Classes Gap': 0}

        self.all_malus_cause = self.complile_malus(student_malus_cause)

        # For each student
        for student in student_list:

            # Compute the malus
            student.compute_malus(self)

            # Add this to the complete malus counter
            self.malus_count += student.malus_count

            # Add this to the complete malus counter
            self.all_malus_cause['Classes Gap'] += student.malus_cause['Classes Gap']


    def complile_malus(self, student_malus):
        return help_function.merge(self.malus_cause, student_malus)


    def find_best_room(attending, rooms):
        # For each room in the list of objects
        for room in rooms:

            # Set high number
            old_difference = 999
            new_difference = abs(attending - room.capacity)

            if new_difference < old_difference:
                selected_room = room
                old_difference = new_difference

        return selected_room


    def fill_schedule_random(self, course, class_type, count, attending):
        """ This function fills a schedule with no student restraints. If there are no rooms available it prints an Error message."""

        # Make key if not existent
        if course.name not in self.schedule:
            self.schedule[course.name] = {}

        succes = False
        while not succes:
            room = random.choice(self.rooms)
            day = random.choice(list(room.availability.keys()))
            timeslot = random.choice(list(room.availability[day].keys()))

            # If timeslot is available
            if room.availability[day][timeslot]:

                self.schedule[course.name][f'{class_type} {count}'] = {}
                clas_number = f"{class_type} {count}"
                schedule_fill.place_in_schedule(self, room, day, timeslot, course.name, clas_number)

                self.check_malus(timeslot, room.capacity, attending)
                succes = True


    def fill_schedule(self, course, class_type, count, attending):
        """ This function fills a schedule with no student restraints. If there are no rooms available it prints an Error message."""

        # Make key if not existent
        if course.name not in self.schedule:
            self.schedule[course.name] = {}

        # For each room in the list of objects
        for room in self.rooms:

            # For each day in its availability
            for day in room.availability:

                # For each timeslot
                for timeslot in room.availability[day]:

                    # If timeslot is availibale
                    if room.availability[day][timeslot]:

                        self.schedule[course.name][f'{class_type} {count}'] = {}
                        clas_number = f"{class_type} {count}"
                        schedule_fill.place_in_schedule(self, room, day, timeslot, course.name, clas_number)

                        self.check_malus(timeslot, room.capacity, attending)
                        return

        # If there are no rooms available at all
        print("Error. No Room!!!")


    def check_malus(self, timeslot, capacity, attending):
        """
        This function checks if a course group is in the late timeslot and 
        whether the amount of attending students is higher then the capacity of that room.
        It then increases the maluspoints respectively.
        """

        # penalty for late night lesson
        if timeslot == 17:
            self.malus_cause['Night'] += 5
            self.malus_count += 5

        # penalty for capacity shortage
        if attending > capacity:
            self.malus_cause['Capacity'] += attending - capacity
            self.malus_count += attending - capacity