from data import *
from assign import *
from main import student_list, roster

# Make lists to put into schedule dataframe
df_list_students = []
df_list_courses = []
df_list_type = []
df_list_rooms = []
df_list_day = []
df_list_time = []

abscent_courses = []

# For each student:
for i, student in enumerate(student_list):

    # For each course the student is enrolled at
    for course in student.courses:

        # If the course does not exist in course list save
        # THIS IS AN ERROR AND NEEDS FIXING
        if course not in roster.schedule:
            abscent_courses.append(course)
            continue

        # For each class:
        for classes in range(1, len(roster.schedule[course]) + 1):

            # Set the current class
            current_class = roster.schedule[course][f'Class {classes}']

            # Add all relevant information ito lists
            df_list_students.append(f'{student.f_name} {student.l_name}')
            df_list_courses.append(course)
            df_list_type.append(current_class['type'])
            df_list_rooms.append(current_class['room'])
            df_list_day.append(current_class['day'])
            df_list_time.append(current_class['timeslot'])

print(set(abscent_courses))

# Create schedule
schedule = pd.DataFrame({'Student': df_list_students,
                         'Course': df_list_courses,
                         'Activity': df_list_type,
                         'Room': df_list_rooms,
                         'Day': df_list_day,
                         'Time': df_list_time})

if __name__ == "__main__":
    print(schedule)