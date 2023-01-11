from data import *
from assign import *
from main import roster

# print(ROOMS)
# print(STUDENT_COURSES)
# print(COURSES)

course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

# Make lists to put into schedule dataframe
df_list_students = []
df_list_courses = []
df_list_type = []
df_list_rooms = []
df_list_day = []
df_list_time = []

# For each course
for i, course in enumerate(course_list):

    # For the amount of classes in each course
    for classes in range(1, len(roster.schedule[course.name]) + 1):

        # Set the current class
        current_class = roster.schedule[course.name][f'Class {classes}']

        # Add all relevant information ito lists
        df_list_students.append('Work in Progress')
        df_list_courses.append(course.name)
        df_list_type.append(current_class['type'])
        df_list_rooms.append(current_class['room'])
        df_list_day.append(current_class['day'])
        df_list_time.append(current_class['timeslot'])

# Create schedule
schedule = pd.DataFrame({'Student': df_list_students,
                         'Course': df_list_courses,
                         'Activity': df_list_type,
                         'Room': df_list_rooms,
                         'Day': df_list_day,
                         'Time': df_list_time})

if __name__ == "__main__":
    print(schedule)