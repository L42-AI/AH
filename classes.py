# Self schedule argument
# Self cost arguement

class Student():
    def __init__(self, info):
        """ Initialize attributes of class from data """

        # Set attributes
        self.f_name = info['Voornaam']
        self.l_name = info['Achternaam']
        self.id = info['Stud.Nr.']

        # create a list with courses that a student follows
        self.courses = [course for course in info[3:] if str(course) != 'nan']

    def add_courses(self, courses):
        """ Assign all the courses to the student and set the enrollment dictionary """

        # For each course:
        for course in courses:

            # Add courses to the courses list
            self.courses.append(course)


class Course():
    # *arg toevoegen
    def __init__(self, course):
        """ Initialize attributes of class from data """

        # Set attributes
        self.name = course['Vak']
        self.lectures = course['#Hoorcolleges']
        self.tutorials = course['#Werkcolleges']
        self.tutorial_rooms = 0
        self.max_std = course['Max. stud. Werkcollege']
        self.practica = course['#Practica']
        self.practica_rooms = 0
        self.max_std_practica = course['Max. stud. Practicum']
        self.expected = course['Verwacht']
        self.rooms_needed()
    
    def rooms_needed(self):
        
        if self.tutorials != 0:
            self.tutorial_rooms = int(self.expected / self.max_std + 1)
        if self.practica != 0:
            self.practica_rooms = int(self.expected / self.max_std_practica + 1)
            print(f"check {self.name} {self.practica_rooms}")
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
        timeslots = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']

        # For each day:
        for day in days:

            # If not yet in availability:
            if day not in self.availability:

                # Set key
                self.availability[day] = {}

            # For each timeslot
            for timeslot in timeslots:

                # Set availability to True
                self.availability[day][timeslot] = True


class Roster():
    def __init__(self, rooms):
        """ Initialize attributes of class """
        self.schedule = {}
        self.rooms = rooms
        self.cost = float


    def fill_schedule(self, course, class_type, scheduled_classes):
        """" This function fills a schedule with with no student restraints """

        # Make key if not existent
        if course.name not in self.schedule:
            self.schedule[course.name] = {}

        # For each room in the list of objects
        for room in self.rooms:

            # For each day in its availability
            for day in room.availability:

                # For each timeslot
                for timeslot in room.availability[day]:

                    # If timeslot is availibale (True):
                    if room.availability[day][timeslot]:

                        # Increase scheduled_classes count
                        scheduled_classes += 1

                        # Create dictionary and add all keys
                        self.schedule[course.name][f'Class {scheduled_classes}'] = {}
                        self.schedule[course.name][f'Class {scheduled_classes}']['day'] = day
                        self.schedule[course.name][f'Class {scheduled_classes}']['timeslot'] = timeslot
                        self.schedule[course.name][f'Class {scheduled_classes}']['type'] = class_type
                        self.schedule[course.name][f'Class {scheduled_classes}']['room'] = room.id

                        room.availability[day][timeslot] = False
                        return
                  

                        
