"""
This file includes the class Course which represents a course.
The data used comes from the given dataframe.
The class includes 5 methods.
add_courses and pick_group are part of the initialisation.
student_timeslot, malus_point are two methods to compute the malus points.
compute_malus runs these functions.
"""

class Course():

    def __init__(self, data, enrolled):

        # Set the lectures from the given data
        self.name = data['Vak']
        self.lectures = data['#Hoorcolleges']
        self.enrolled = enrolled

        # Set the attributes about the tutorials
        self.tutorials = data['#Werkcolleges']
        self.max_std = data['Max. stud. Werkcollege']
        self.tutorial_rooms = 0

        # Set the attributes about the practica
        self.practicals = data['#Practica']
        self.max_std_practical = data['Max. stud. Practicum']
        self.practical_rooms = 0

        # initiate the libararies
        self.tut_group_dict = {}
        self.pract_group_dict = {}

        # Run initializing functions
        self.rooms_needed()
        self.group_dict()

    def __str__(self):
        return f"{self.name}"

    def rooms_needed(self):

        # only create groups when there are tutorials and practical
        if self.tutorials != 0:
            self.tutorial_rooms = int(self.enrolled / self.max_std)

            # int cuts 3.1 to 3, but 3.1 would require 4 groups
            if self.enrolled % self.max_std != 0:
                self.tutorial_rooms += 1

        if self.practicals != 0:
            self.practical_rooms = int(self.enrolled / self.max_std_practical)
            if self.enrolled % self.max_std_practical != 0:
                self.practical_rooms += 1

    def group_dict(self):

        for i in range(self.tutorial_rooms):
            self.tut_group_dict[i + 1] = 0

        for i in range(self.practical_rooms):
            self.pract_group_dict[i + 1] = 0

