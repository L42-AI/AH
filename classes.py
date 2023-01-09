'''a student will have 'course' and 'name' as an argument. 
    enrollment will be the course and the assigned tutorial
'''

class Student():
    def __init__(self, info):

        self.f_name = info['Voornaam']
        self.l_name = info['Achternaam']
        self.id = info['Stud.Nr.']
        self.courses = [course for course in info if str(course).startswith("Vak")]

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
    def __init__(self):
        pass

    def assign_tutorial(self):
        pass