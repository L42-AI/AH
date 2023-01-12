import random

class Student():
    def __init__(self, info, courses):
        """ Initialize attributes of class from data """

        # Set attributes
        self.f_name = info['Voornaam']
        self.l_name = info['Achternaam']
        self.id = info['Stud.Nr.']

        # create a list with courses that a student follows
        # self.course_names holds the strings, self.course holds the objects
        self.courses_names = [course for course in info[3:] if str(course) != 'nan']
        self.courses = []
        self.tut_group = None
        self.pract_group = None
        self.timeslots = []
        self.add_courses(courses)
        self.pick_group()


    def __str__(self):
        return f"{self.f_name} {self.l_name}"

    def student_cost(self, Roster):

        # first get all the education moments
        
        for course in self.courses:
            for index in range(course.lectures):
                self.timeslots.append(Roster.schedule[course.name][f"lecture {index + 1}"])

            for index in range(course.tutorials):

                # tut*index is incase group needs 2 tutorials, so they need timeslots from 2 entries
                self.timeslots.append(Roster.schedule[course.name][f"tutorial {(self.tut_group + self.tut_group * index)}"])

            for index in range(course.practica):
                self.timeslots.append(Roster.schedule[course.name][f"practical {(self.pract_group + self.pract_group * index)}"])
        
        self.same_day()
    
    def same_day(self):
        days = []
        count = {}
        for timeslot in self.timeslots:
            days.append(timeslot['day'])
        
        for day in days:
            if day in count:
                count[day] += 1
            else:
                count[day] = 1

        print(days)
  
        self.timeslots = [day for day in days if count[day] > 1]

        # dict van maken met als values een lijst met daarin de timeslots
        print(self.timeslots)

    def add_courses(self, courses):
        """ Assign all the courses to the student and set the enrollment dictionary """

        # For each course:
        for name in self.courses_names:

            # Add courses to the courses list
            for course in courses:
                if course.name == name:
                    self.courses.append(course)

    def pick_group(self):

        # go over all the courses a student is in 
        for course in self.courses:

            ### does not work! I will fix tomorrow! course = string not the object
            if course.tutorials != 0:
                dict = course.tut_group_dict
                possible_groups = list(dict)[-1]
                group_picked = False

                # keep looking for a group untill student finds one with room
                while not group_picked:
                    group_picked = random.randint(1, possible_groups)
                    if dict[group_picked] < course.max_std:
                        course.tut_group_dict[group_picked] += 1
                        self.tut_group = group_picked
                    else:
                        group_picked = False

            if course.practica != 0:
                dict = course.pract_group_dict
                possible_groups = list(dict)[-1]
                group_picked = False

                # keep looking for a group untill student finds one with room
                while not group_picked:
                    group_picked = random.randint(1, possible_groups)
                    if dict[group_picked] < course.max_std_practica:
                        course.pract_group_dict[group_picked] += 1
                        self.pract_group = group_picked
                    else:
                        group_picked = False


class Course():

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
        self.group_dict()

    def __str__(self):
        return f"{self.name}"

    def rooms_needed(self):

        # only create groups when there are tutorials and practica
        if self.tutorials != 0:
            self.tutorial_rooms = int(self.expected / self.max_std)

            # int cuts 3.1 to 3, but 3.1 would require 4 groups
            if self.expected % self.max_std != 0:
                self.tutorial_rooms += 1

        if self.practica != 0:
            self.practica_rooms = int(self.expected / self.max_std_practica)
            if self.expected % self.max_std_practica != 0:
                self.practica_rooms += 1

    def group_dict(self):

        self.tut_group_dict = {}
        for i in range(self.tutorial_rooms):
            self.tut_group_dict[i + 1] = 0

        self.pract_group_dict = {}
        for i in range(self.practica_rooms):
            self.pract_group_dict[i + 1] = 0


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
            break

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
                        return