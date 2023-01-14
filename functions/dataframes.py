"""
This file contains a function that transforms the schedule into a excel
"""

import pandas as pd

def schedule_dataframe(Roster, student_list):
    # Make lists to put into schedule dataframe
    df_list_student_malus = []
    df_list_students = []
    df_list_courses = []
    df_list_type = []
    df_list_rooms = []
    df_list_day = []
    df_list_time = []

    # For each student:
    for student in student_list:

        # For each course the student is enrolled at
        for course in student.courses:

            # For each class:
            for class_name in Roster.schedule[course.name]:

                current_class = Roster.schedule[course.name][class_name]

                # Add all relevant information ito lists
                df_list_student_malus.append(student.malus)
                df_list_students.append(f'{student.f_name} {student.l_name}')
                df_list_courses.append(course)
                df_list_rooms.append(current_class['room'])
                df_list_day.append(current_class['day'])
                df_list_time.append(current_class['timeslot'])
                df_list_type.append(class_name)

    # Create schedule
    schedule_df = pd.DataFrame({'Student': df_list_students,
                                'Course': df_list_courses,
                                'Activity': df_list_type,
                                'Room': df_list_rooms,
                                'Day': df_list_day,
                                'Time': df_list_time,
                                'Student Malus': df_list_student_malus,
                                'Total Malus': Roster.malus})
    return schedule_df