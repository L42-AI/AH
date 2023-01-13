import classes.course as CourseClass
import classes.room  as RoomClass
import classes.student as StudentClass
import functions.count as counts
import re

def assign(COURSES, STUDENT_COURSES, ROOMS):
    '''fill in lists and dictionaries with instances'''
    course_list = []
    student_list = []
    rooms = []
    dict_enrollment = counts(STUDENT_COURSES)

    # create an instance for every course
    for _, course in COURSES.iterrows():

        # because the data in vakken.csv is not the same as in student_en_vakken.csv
        # we choose to put in this regex
        course_name = re.sub(r',', "", str(course['Vak']))

        # fill in the list with course objects 
        course_list.append(CourseClass(course, dict_enrollment[course_name]))

    for _, student in STUDENT_COURSES.iterrows():

        # fill in the list with student objects
        student_list.append(StudentClass(student, course_list))

    for _, room in ROOMS.iterrows():

        # fill in the list with room objects
        rooms.append(RoomClass(room))

    return course_list, student_list, rooms

