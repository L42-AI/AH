from classes import *
from data import COURSES, ROOMS, STUDENT_COURSES

'''assign all classes'''


def assign(COURSES, ROOMS, STUDENT_COURSES):
    '''fill in lists and dictionaries with instances'''
    course_list = []
    student_list = []
    rooms = {}

    for _, course in COURSES.iterrows():

        # create an instance for every course
        course_list.append(Course(course))

    for _, student in STUDENT_COURSES.iterrows():

        # fill in the list with student instances
        student_list.append(Student(student))

    for _, room in ROOMS.iterrows():

        # fill the dict with room numbers, and their occupational status
        rooms[room['Zaalnummber']] = 'free'

    return course_list, student_list, rooms