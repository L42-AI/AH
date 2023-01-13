import classes.course as CourseClass
import classes.room  as RoomClass
import classes.student as StudentClass
import functions.count as counts

def assign(COURSES, STUDENT_COURSES, ROOMS):
    '''fill in lists and dictionaries with instances'''
    course_list = []
    student_list = []
    rooms = []
    enrollment = counts.count_students(STUDENT_COURSES)

    # create an instance for every course
    for _, course in COURSES.iterrows():

        # Zoeken, sturen en bewegen has "" in the name so can't be found when looking in dict
        ## therefore explicit argument is needed
        try:
            course_list.append(CourseClass.Course(course, enrollment[course['Vak']]))
        except:
            course_list.append(CourseClass.Course(course, 42))

    for _, student in STUDENT_COURSES.iterrows():

        # fill in the list with student instances
        student_list.append(StudentClass.Student(student, course_list))

    for _, room in ROOMS.iterrows():

        rooms.append(RoomClass.Room(room))

    return course_list, student_list, rooms

