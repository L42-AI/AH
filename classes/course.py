class Course():

    def __init__(self, course, enrolled):
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
        self.enrolled = enrolled
        self.rooms_needed()
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

