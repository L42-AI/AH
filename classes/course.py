"""
This file includes the class Course which represents a course.
The data used comes from the given dataframe.
The class includes 5 methods.
add_courses and pick_group are part of the initialisation.
student_timeslot, malus_point are two methods to compute the malus points.
compute_malus runs these functions.
"""

from functions.count_students import *

class Course():

    def __init__(self, data, enrolled):

        # Set from the given data
        self.name = data['Vak']
        self.lectures = data['#Hoorcolleges']

        # Set the attributes about the tutorials
        self.tutorials = data['#Werkcolleges']
        self.max_std = data['Max. stud. Werkcollege']
        self.tutorial_rooms = 0

        # Set the attributes about the practica
        self.practica = data['#Practica']
        self.max_std_practica = data['Max. stud. Practicum']
        self.practica_rooms = 0

        self.rooms_needed()

        self.enrolled = enrolled

        self.group_dict()

    def __str__(self):
        return f"{self.name}"

    def rooms_needed(self):

        # only create groups when there are tutorials and practica
        if self.tutorials != 0:
            self.tutorial_rooms = int(self.enrolled / self.max_std)

            # int cuts 3.1 to 3, but 3.1 would require 4 groups
            if self.enrolled % self.max_std != 0:
                self.tutorial_rooms += 1

        if self.practica != 0:
            self.practica_rooms = int(self.enrolled / self.max_std_practica)
            if self.enrolled % self.max_std_practica != 0:
                self.practica_rooms += 1

    def group_dict(self):

        self.tut_group_dict = {}
        for i in range(self.tutorial_rooms):
            self.tut_group_dict[i + 1] = 0

        self.pract_group_dict = {}
        for i in range(self.practica_rooms):
            self.pract_group_dict[i + 1] = 0

