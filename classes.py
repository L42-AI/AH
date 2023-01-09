'''a student will have 'course' and 'name' as an argument. 
    enrollment will be the course and the assigned tutorial
'''

class Student():
    def __init__(self, last_name, first_name, id, courses):

        self.name = f'{first_name} {last_name}'
        self.id = id

        # Set a list for the courses the student takes
        self.courses = []

        # here the results will be stored
        self.enrollment = {}

        # Run add_courses to add all courses to each student
        self.add_courses(courses)

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
    def __init__(self, name, lectures, tutorials, max_std, practicals, estimated_std):
        self.name = name = str

        self.lectures = lectures = int
        self.tutorials = tutorials = int
        self.practicals = practicals = int
        self.max_std = max_std = int

        self.estimated_std = estimated_std = int



class Roster():
    def __init__(self):
        pass

    def assign_tutorial(self):
        pass