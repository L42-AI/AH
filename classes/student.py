import copy 
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
        self.schedule = []
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
        
        # make the schedule before timeslots gets editted
        self.schedule = copy.deepcopy(self.timeslots)
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