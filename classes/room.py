# This class Room takes its data from a dataframe that it is initialized with.
# It then Makes a dictionary with key the weekdays and value another dictionary.
# The nested dictionary has the timeslots as keys and True as value. True means the room is available.

import random


class Room():
    def __init__(self, room):
        # Set attributes from the dataframe room
        self.id = room['Zaalnummber']
        self.capacity = room['Max. capaciteit']
        self.availability = {}

        # Run initializing funciton
        self.initialize_availability()

    def initialize_availability(self):
        """ Set availability of all rooms in a random order for days and timeslots"""

        # Set lists of days and times
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        timeslots = [9, 11, 13, 15]
        timeslots_biggest = [9, 11, 13, 15, 17]

        # shuffle the days and timeslots for the random initiate
        random.shuffle(days)
        random.shuffle(timeslots)
        random.shuffle(timeslots_biggest)

        # Loop over each day and 
        for day in days:

            # check if it is the biggest room, if so use other timeslots
            if self.id == 'C0.110':
                timeslots = timeslots_biggest

            # If not yet in availability:
            if day not in self.availability:

                # Set key
                self.availability[day] = {}

            # For each timeslot
            for timeslot in timeslots:

                # Set availability to True
                self.availability[day][timeslot] = True
