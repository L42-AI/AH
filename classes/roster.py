import random


class Roster():
    def __init__(self, rooms):
        """ Initialize attributes of class """
        self.schedule = {}
        self.rooms = rooms
        random.shuffle(self.rooms)
        self.cost = 0

    def total_cost(self, student_list):
        for student in student_list:

            student.student_cost(self)
            self.cost += student.malus
        


    def fill_schedule(self, course, class_type, count, attending):
        """" This function fills a schedule with with no student restraints """

        # Make key if not existent
        if course.name not in self.schedule:
            self.schedule[course.name] = {}

        # For each room in the list of objects
        for room in self.rooms:
            days = list(room.availability.keys())
            random.shuffle(days)

            # For each day in its availability
            for day in days:
                timeslots = list(room.availability[day].keys())
                random.shuffle(timeslots)

                # For each timeslot
                for timeslot in timeslots:

                    # If timeslot is availibale and capacity is good
                    if room.availability[day][timeslot]:

                        # Create dictionary and add all keys
                        self.schedule[course.name][f'{class_type} {count}'] = {}
                        self.schedule[course.name][f'{class_type} {count}']['day'] = day
                        self.schedule[course.name][f'{class_type} {count}']['timeslot'] = timeslot
                        self.schedule[course.name][f'{class_type} {count}']['room'] = room.id

                        self.cost += (attending - room.capacity) if attending > room.capacity else 0

                        room.availability[day][timeslot] = False

                        self.check_malus(timeslot, room.capacity, attending)
                        return
        print("No Room!!")

    def check_malus(self, timeslot, capacity, attending):

        # penalty for late night lesson
        if timeslot == 17:
            self.cost += 5
        
        # penalty for capacity shortage
        if attending > capacity:
            self.cost += attending - capacity
