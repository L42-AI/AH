import classes.course as CourseClass
import classes.room  as RoomClass
import classes.student as StudentClass
from functions.count import count_students
import re
from data import COURSES, ROOMS, STUDENT_COURSES

def assign(COURSES, STUDENT_COURSES, ROOMS):
    """This Function takes in 3 Dataframes, loops over the dataframe and fills a list with the respective Class objects."""

    course_list = []
    student_list = []
    rooms = []

    # count the students that have enrolled for each course
    dict_enrollment = count_students(STUDENT_COURSES)

    # create an instance for every course
    for _, course in COURSES.iterrows():

        # fill in the list with course objects 
        course_list.append(CourseClass.Course(course, dict_enrollment[course['Vak']]))

    for _, student in STUDENT_COURSES.iterrows():

        # fill in the list with student objects
        student_list.append(StudentClass.Student(student, course_list))

    for _, room in ROOMS.iterrows():

        # fill in the list with room objects
        rooms.append(RoomClass.Room(room))

    return course_list, student_list, rooms

