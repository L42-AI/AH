# Self schedule argument
# Self cost arguement
# Self schedule argument
# Self cost arguement
class Student():
    def __init__(self, info):

        self.f_name = info['Voornaam']
        self.l_name = info['Achternaam']
        self.id = info['Stud.Nr.']

        # create a list with courses that a student follows
        self.courses = [course for course in info[3:] if str(course) != 'nan']
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
        self.name = course['Vak']
        self.name = course['Vak']
        self.lectures = course['#Hoorcolleges']
        self.tutorials = course['#Werkcolleges']
        self.max_std = course['Max. stud. Werkcollege']
        self.tutorials = course['#Werkcolleges']
        self.max_std = course['Max. stud. Werkcollege']
        self.practica = course['#Practica']
        self.max_std_practica = course['Max. stud. Practicum']
        self.max_std_practica = course['Max. stud. Practicum']
        self.expected = course['Verwacht']

class Room():
    def __init__(self, room):
        self.id = room['Zaalnummber']
        self.capacity = room['Max. capaciteit']
        self.availability = {}

        self.initialize_availability()

    def initialize_availability(self):
        self.availability = {}

        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            if day not in self.availability:
                self.availability[day] = {}
            for timeslot in ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']:
                self.availability[day][timeslot] = True


class Roster():
    def __init__(self, rooms):
        self.schedule = {} # moet plus zijn en niet overschrijven, meerder values per vak
        self.rooms = rooms


    def fill_schedule(self, name, type):
        # capacity and schedule logic is not important for now
        for room in self.rooms:
            for day in room.availability:
                for timeslot in room.availability[day]:
                    if room.availability[day][timeslot]:
                        if name in self.schedule:
                            self.schedule[name] += f"{type} in  {room.id} on {day} at {timeslot}."
                        else:
                            self.schedule[name] = f"{type} in  {room.id} on {day} at {timeslot}."
                        
                        room.availability[day][timeslot] = False
