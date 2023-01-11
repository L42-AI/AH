from assign import *
from classes import *
from data import *

course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

## this can go in assign ##
for course in course_list:

    # first calculate groups needed
    groups_tut = int((course.expected / course.max_std) + 1)
    groups_pract = int((course.expected / course.max_std_practica) + 1)

    for student in student_list