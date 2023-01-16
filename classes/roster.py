# This class takes in a list of objects called rooms and makes a roster. 
# It can also calculate the total amount maluspoints

import random
import functions.helpers as help_function

class Roster():
    def __init__(self, rooms):
        self.schedule = {}
        self.rooms = rooms

        self.malus = {}
        self.init_malus()

        # shuffle the list of room object for the random initialze
        random.shuffle(self.rooms)

    def init_malus(self):
        self.malus['Night'] = 0
        self.malus['Capacity'] = 0

    def total_malus(self, student_list):
        """This function loops over the list filled with Student objects and calculates the total maluspoints"""
        
        student_malus = {'Classes Gap': 0}

        self.complete_malus = self.complile_malus(student_malus)

        # For each student
        for student in student_list:

            # Compute the malus
            student.compute_malus(self)

            # Add this to the complete malus counter
            self.complete_malus['Classes Gap'] += student.malus['Classes Gap']

        self.complile_malus(student_malus)

    def complile_malus(self, student_malus):

        return help_function.merge(self.malus, student_malus)

    def fill_schedule(self, course, class_type, count, attending):
        """ This function fills a schedule with no student restraints. If there are no rooms available it prints an Error message."""

        print('\nAttending:')
        print(attending)
        print()

        # Make key if not existent
        if course.name not in self.schedule:
            self.schedule[course.name] = {}

        # For each room in the list of objects
        for room in self.rooms:

            print(f'\n{room.id}')
            print(room.capacity)
            print()

            # For each day in its availability
            for day in room.availability:

                # For each timeslot
                for timeslot in room.availability[day]:

                    # If timeslot is availibale
                    if room.availability[day][timeslot]:

                        # Create dictionary and add all keys
                        self.schedule[course.name][f'{class_type} {count}'] = {}
                        self.schedule[course.name][f'{class_type} {count}']['day'] = day
                        self.schedule[course.name][f'{class_type} {count}']['timeslot'] = timeslot
                        self.schedule[course.name][f'{class_type} {count}']['room'] = room.id

                        room.availability[day][timeslot] = False

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
            self.malus['Night'] += 5

        # penalty for capacity shortage
        if attending > capacity:
            self.malus['Capacity'] += attending - capacity