from data.data import COURSES, STUDENT_COURSES, ROOMS
import classes.representation.course as CourseClass
import classes.representation.student as StudentClass
import classes.representation.room as RoomClass

def assign(COURSES, STUDENT_COURSES, ROOMS):
    """This Function takes in 3 Dataframes, loops over the dataframe and fills a list with the respective Class objects."""

    global course_list, student_list, room_list

    course_list = []
    student_list = []
    room_list = []

    # count the students that have enrolled for each course
    dict_enrollment = __count_students(STUDENT_COURSES)

    # create an instance for every course
    for _, course in COURSES.iterrows():

        # fill in the list with course objects
        course_list.append(CourseClass.Course(course, dict_enrollment[course['Vak']]))

    for _, student in STUDENT_COURSES.iterrows():

        # fill in the list with student objects
        student_list.append(StudentClass.Student(student, course_list))

    for _, room in ROOMS.iterrows():

        # fill in the list with room objects
        room_list.append(RoomClass.Room(room))

    for course in course_list:
        course.enroll_students(student_list)
        course.flag_hard_student(student_list)

def __count_students(dataframe):
    """This function Counts the amount of students enrolled for each course"""

    list_courses = ['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']
    dict_count = {}

    # loop over each row of the dataframe and set the count plus 1
    for _, row in dataframe.iterrows():
        for course in list_courses:

            # make it a string, in order to easily check if it is nan
            course_str = str(row[course])

            if course_str != 'nan':

                # check if its in the dict, if not make a key and set value to 0
                if course_str not in dict_count:
                    dict_count[course_str] = 0

                # count the students
                dict_count[course_str] += 1

    return dict_count

assign(COURSES, STUDENT_COURSES, ROOMS)