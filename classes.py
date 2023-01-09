'''a student will have 'course' and 'name' as an argument. 
    enrollment will be the course and the assigned tutorial
'''

class Student():
    def __init__(self, last_name, first_name, std_numb, course):

        # course will be a list
        self.course = course
        self.last_name = last_name
        self.first_name = first_name
        self.std_numb = std_numb

        # here the results will be stored
        self.enrollment = {}



class Course():
    # *arg toevoegen
    def __init__(self, name, lectures, tutorials, max_std, practical, estimated_std):
        self.name = name
        self.lectures = lectures
        self.tutorials = tutorials
        self.max_std = max_std
        self.practical = practical
        self.estimated_std = estimated_std



class Roster():
    def __init__(self):
        pass

    def assign_tutorial(self):
        pass