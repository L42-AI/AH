import copy 
import random

class Student():
    def __init__(self, input, courses):
        """ Initialize attributes of class from data """

        # Set attributes
        self.f_name = input['Voornaam']
        self.l_name = input['Achternaam']
        self.id = input['Stud.Nr.']

        # create a list with courses that a student follows
        # self.course_names holds the strings, self.course holds the objects
        self.courses_names = [course for course in input[3:] if str(course) != 'nan']
        self.courses = []
        self.tut_group = {}
        self.pract_group = {}
        self.timeslots = []
        self.schedule = []
        self.malus = 0
        self.add_courses(courses)
        self.pick_group()

    def __str__(self):
        return f"{self.f_name} {self.l_name}"

    def student_cost(self, Roster):
        # reset malus points so they do not increase over iterations
        self.malus = 0

        # first get all the education moments
        for course in self.courses:
            for index in range(course.lectures):
                self.timeslots.append(Roster.schedule[course.name][f"lecture {index + 1}"])

            for index in range(course.tutorials):
                # tut*index is incase group needs 2 tutorials, so they need timeslots from 2 entries
                self.timeslots.append(Roster.schedule[course.name][f"tutorial {(self.tut_group[course.name] + self.tut_group[course.name] * index)}"])

            for index in range(course.practica):
                # print(self.id)
                # print(self.timeslots)
                # print()
                # print(course.name)
                # print(Roster.schedule[course.name])
                # print(self.pract_group)
                self.timeslots.append(Roster.schedule[course.name][f"practical {(self.pract_group[course.name] + self.pract_group[course.name] * index)}"])

        # make the schedule before timeslots gets editted
        self.schedule = copy.deepcopy(self.timeslots)

        # remove days that only occur once and calc malus
        self.same_day()
        self.malus_points()
        # print(self.timeslots, self.malus)

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
  
        self.timeslots = [timeslot for timeslot in self.timeslots if count[timeslot['day']] > 1]

    def malus_points(self):
        days = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}

        # dictionary that holds the timeslots for every day student has
        for timeslots in self.timeslots:
              days[timeslots['day']].append(timeslots['timeslot'])
        
        for day in days:
            days[day].sort(reverse=True)
            list = days[day]
            
            # only run when there is a list
            if list:
                for i in range(len(list) - 1):

                    # some cases, double booking might be allowed, but we do not want to add 2 malus
                    if list[i] - list[i + 1] != 0:
                        self.malus += int((list[i] - (list[i+1] + 2)) / 2)
        

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
                        self.tut_group[course.name] = group_picked
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
                        self.pract_group[course.name] = group_picked
                    else:
                        group_picked = False