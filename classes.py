# Self schedule argument
# Self cost arguement
class Student():
    def __init__(self, info):

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
        self.name = course['Vak']
        self.lectures = course['#Hoorcolleges']
        self.tutorials = course['#Werkcolleges']
        self.max_std = course['Max. stud. Werkcollege']
        self.practica = course['#Practica']
        self.max_std_practica = course['Max. stud. Practicum']
        self.expected = course['Verwacht']

class Room():
    def __init__(self, room):
        self.id = room['Zaalnummber']
        self.capacity = room['Max. capaciteit']
        self.availability = {}

        self.initialize_availability()

    def initialize_availability(self):
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for timeslot in ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']:
                self.availability[day][timeslot] = True

class Roster():
    def __init__(self):
        pass

    def assign_tutorial(self):
        pass
