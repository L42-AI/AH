from classes.course import *
from classes.room import *
from classes.student import *
from data import COURSES, ROOMS, STUDENT_COURSES

'''assign all classes'''


def assign(COURSES, STUDENT_COURSES, ROOMS):
    '''fill in lists and dictionaries with instances'''
    course_list = []
    student_list = []
    rooms = []

    for _, course in COURSES.iterrows():

        # create an instance for every course
        course_list.append(Course(course))

    for _, student in STUDENT_COURSES.iterrows():

        # fill in the list with student instances
        student_list.append(Student(student, course_list))

    for _, room in ROOMS.iterrows():

        rooms.append(Room(room))

    return course_list, student_list, rooms

