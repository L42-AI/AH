from data import *
from assign import *
from main import roster

# print(ROOMS)
# print(STUDENT_COURSES)
# print(COURSES)

course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

df_list_students = []
df_list_courses = []
df_list_type = []
df_list_rooms = []
df_list_day = []
df_list_time = []

for i, course in enumerate(course_list):
    for classes in range(1, len(roster.schedule[course.name]) + 1):

        current_class = roster.schedule[course.name][f'Class {classes}']

        df_list_students.append(student_list[i].f_name)
        df_list_courses.append(course.name)
        df_list_type.append(current_class['type'])
        df_list_rooms.append(current_class['room'])
        df_list_day.append(current_class['day'])
        df_list_time.append(current_class['timeslot'])

schedule = pd.DataFrame({'Student': df_list_students,
                         'Course': df_list_courses,
                         'Activity': df_list_type,
                         'Room': df_list_rooms,
                         'Day': df_list_day,
                         'Time': df_list_time})
print(schedule['Student'][schedule['Student'] == 'Yanick'])