import classes.course as CourseClass
import classes.room  as RoomClass
import classes.student as StudentClass
from functions.count import count_students

def assign(COURSES, STUDENT_COURSES, ROOMS, LARGEST_FIRST=False):
    """This Function takes in 3 Dataframes, loops over the dataframe and fills a list with the respective Class objects."""

    course_list = []
    student_list = []
    rooms = []

    # count the students that have enrolled for each course
    dict_enrollment = count_students(STUDENT_COURSES)

    if LARGEST_FIRST: 
        sorted_courses = __largest_course(dict_enrollment)
        COURSES =  COURSES.sort_values(by='Vak', key=lambda x: sorted_courses[x])

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

def __largest_course(dict_enrollment):

    # course with largest attendence first
    sorted_d = dict(sorted(dict_enrollment.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_d