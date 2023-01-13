"""
This fule includes the class Room which represents the classrooms
It has one method which is initializing its availablility
"""

import random

class Room():
    def __init__(self, data):

        # Set attributes from data
        self.id = data['Zaalnummber']
        self.capacity = data['Max. capaciteit']

        # Run initializing funciton
        self.availability = {}
        self.initialize_availability()

    def initialize_availability(self):
        """ Set availability of all rooms """

        # Set lists of days and times
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # Set possible timeslots
        timeslots = [9, 11, 13, 15]
        timeslots_biggest = [9, 11, 13, 15, 17]

        # Randomly shuffle all lists
        random.shuffle(days)
        random.shuffle(timeslots)
        random.shuffle(timeslots_biggest)

        # For each day:
        for day in days:

            # Check if it is the biggest room
            if self.id == 'C0.110':

                # use other timeslot list
                timeslots = timeslots_biggest

            # If not yet in availability:
            if day not in self.availability:

                # Set key
                self.availability[day] = {}

            # For each timeslot
            for timeslot in timeslots:

                # Set availability to True
                self.availability[day][timeslot] = True
