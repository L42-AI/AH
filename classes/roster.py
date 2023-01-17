# This class takes in a list of objects called rooms and makes a roster. 
# It can also calculate the total amount maluspoints
import functions.schedule_fill as schedule_fill
import random

class Roster():
    def __init__(self, rooms):
        self.schedule = {}
        self.rooms = rooms
        self.malus = 0

        # shuffle the list of room object for the random initialze
        random.shuffle(self.rooms)

    def total_malus(self, student_list):
        """This function loops over the list filled with Student objects and calculates the total maluspoints"""

        # loop over each student and add to the total
        for student in student_list:

            student.compute_malus(self)
            self.malus += student.malus

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
            self.malus += 5
        
        # penalty for capacity shortage
        if attending > capacity:
            self.malus += attending - capacity
