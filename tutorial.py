from assign import *
from classes import *
from data import *

course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

## this can go in assign ##
for course in course_list:
    print(course)
    # first calculate groups needed
    print(course.expected, course.max_std)
    if course.tutorials != 0:
        number_groups_tut = int((course.expected / course.max_std) + 1)
        groups_tut = split(course.expected, number_groups_tut)
        print(groups_tut)
    if course.practica != 0:
        number_groups_pract = int((course.expected / course.max_std_practica) + 1)
        groups_pract = split(course.expected, number_groups_pract)
        
    


