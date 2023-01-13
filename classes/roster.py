import random

class Roster():
    def __init__(self, rooms):
        """ Initialize attributes of class """
        self.schedule = {}
        self.rooms = rooms
        self.cost = 0

        # shuffle the list of room object for the random initialze
        random.shuffle(self.rooms)

    def total_cost(self, student_list):
        for student in student_list:

            student.student_cost(self)
            self.cost += student.malus

    def fill_schedule(self, course, class_type, count, attending):
        """" This function fills a schedule with no student restraints"""

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

        # penalty for late night lesson
        if timeslot == 17:
            self.cost += 5
        
        # penalty for capacity shortage
        if attending > capacity:
            self.cost += attending - capacity
