# This function 

from classes.course import *
from classes.room import *
from classes.student import *
from functions.count_students import *
from data import COURSES, ROOMS, STUDENT_COURSES
import re


def assign(COURSES, STUDENT_COURSES, ROOMS):
    '''fill in lists and dictionaries with instances'''
    course_list = []
    student_list = []
    rooms = []
    dict_enrollment = count_students(STUDENT_COURSES)

    # create an instance for every course
    for _, course in COURSES.iterrows():

        # because the data in vakken.csv is not the same as in student_en_vakken.csv
        # we choose to put in this regex
        course_name = re.sub(r',', "", str(course['Vak']))

        # fill in the list with course objects 
        course_list.append(Course(course, dict_enrollment[course_name]))

    for _, student in STUDENT_COURSES.iterrows():

        # fill in the list with student objects
        student_list.append(Student(student, course_list))

    for _, room in ROOMS.iterrows():

        # fill in the list with room objects
        rooms.append(Room(room))

    return course_list, student_list, rooms

