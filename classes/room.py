import random

class Room():
    def __init__(self, room):
        """ Initialize attributes of class from data """

        # Set attributes
        self.id = room['Zaalnummber']
        self.capacity = room['Max. capaciteit']
        self.availability = {}

        # Run initializing funciton
        self.initialize_availability()

    def initialize_availability(self):
        """ Set availability of all rooms """

        # Set lists of days and times
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        timeslots = [9, 11, 13, 15]
        timeslots_biggest = [9, 11, 13, 15, 17]
        random.shuffle(days)
        random.shuffle(timeslots)
        random.shuffle(timeslots_biggest)

        # For each day:
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
