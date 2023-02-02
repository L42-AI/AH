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
        self.enrolled_students = set()
        self.lecture_day = None

        # Set the attributes about the tutorials
        self.tutorials = data['#Werkcolleges']
        self.max_std_tutorial = data['Max. stud. Werkcollege']
        self.tutorial_rooms = 0

        # Set the attributes about the practica
        self.practicals = data['#Practica']
        self.max_std_practical = data['Max. stud. Practicum']
        self.practical_rooms = 0

        # initiate the libararies
        self.tut_group_dict = {}
        self.pract_group_dict = {}
        self.capacity_malus = 0

        # Run initializing function 
        self.rooms_needed()
        self.group_dict()

        # heuristic to prioritise course if it has students that have complex schedule
        self.prioritise = False

    def __str__(self):
        return f"{self.name}"

    def enroll_students(self, student_list):
        """
        This method goes over each students courses,
        and adds them to a enrolled set per course
        """

        # for each student:
        for student in student_list:
            # for each of the student's courses
            for course in student.courses:
                # add to set if student's course equals self

                if course.name == self.name:
                    self.enrolled_students.add(student)

    def flag_hard_student(self, student_list):
        """
        This method goes over each students courses,
        checks if the student in this course is a busy student,
        and flag the course.
        """

        # for each student
        for student in student_list:

            # check if student in course enrolled
            if student in self.enrolled_students and len(student.courses) > 4:

                # Flag course as priority
                self.prioritise = True

    def rooms_needed(self):
        """
        This method finds the amount of seminar rooms needed per course
        """

        # only create groups when there are tutorial
        if self.tutorials != 0:
            self.tutorial_rooms = int(self.enrolled / self.max_std_tutorial)

            # int cuts 3.1 to 3, but 3.1 would require 4 groups
            if self.enrolled % self.max_std_tutorial != 0:
                self.tutorial_rooms += 1

        # only create groups when there are practical
        if self.practicals != 0:
            self.practical_rooms = int(self.enrolled / self.max_std_practical)

            # int cuts 3.1 to 3, but 3.1 would require 4 groups
            if self.enrolled % self.max_std_practical != 0:
                self.practical_rooms += 1

    def group_dict(self):
        """
        This method makes dictionaries for how many students are present in a seminar
        """
        for i in range(self.tutorial_rooms):
            self.tut_group_dict[i + 1] = 0

        for i in range(self.practical_rooms):
            self.pract_group_dict[i + 1] = 0

