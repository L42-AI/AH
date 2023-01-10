'''a student will have 'course' and 'name' as an argument. 
    enrollment will be the course and the assigned tutorial
'''

class Student():
    def __init__(self, info):

        self.f_name = info['Voornaam']
        self.l_name = info['Achternaam']
        self.id = info['Stud.Nr.']

        # create a list with courses that a student follows
        self.courses = [course for course in info if str(course).startswith("Vak") and course != 'Nan']

        # here the results will be stored
        self.enrollment = {}


    def add_courses(self, courses):
        """ Assign all the courses to the student and set the enrollment dictionary """

        # For each course:
        for course in courses:

            # Add courses to the courses list
            self.courses.append(course)

            # Set the courses as keys in the enrolment dictionary
            self.enrollment[course] : 999

    def assign_tutorial_groups(self):
        """ Assign the student's tutorial group per course """
        pass




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



class Roster():
    def __init__(self, rooms, type):
        self.schedule = {}
        self.rooms = rooms
        self.type = type # this will be lecture, tutorial or practica

    def fill_schedule(self, name, rooms):
        # capacity and schedule logic is not important for now
        for room in self.rooms:
            for day in room.availity:
                for timeslot in room.availability[day]:
                    if room.availability[day][timeslot]:
                        room.availability[day][timeslot] = False
                        self.schedule[name] = f"{room.type} in  {room.id} on {room.availability[day]} at {room.availability[day][timeslot]}"