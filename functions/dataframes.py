"""
This file contains a function that transforms the schedule into a excel
"""

import pandas as pd
import os

def schedule_dataframe(Roster, student_list, visualize=False):
    # Make lists to put into schedule dataframe
    df_list_student_object = []
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
        for timeslot in student.timeslots:

            # Add all relevant information ito lists
            df_list_student_object.append(student)
            df_list_student_malus.append(int(student.malus.get('Classes Gap')))
            df_list_students.append(f'{student.f_name} {student.l_name}')
            df_list_courses.append(timeslot['course'])
            df_list_type.append(timeslot['class'])
            df_list_rooms.append(timeslot['room'])
            df_list_day.append(timeslot['day'])
            df_list_time.append(timeslot['timeslot'])


    # Create schedule
    schedule_df = pd.DataFrame({'Object': df_list_student_object,
                                'Student': df_list_students,
                                'Course': df_list_courses,
                                'Activity': df_list_type,
                                'Room': df_list_rooms,
                                'Day': df_list_day,
                                'Time': df_list_time,
                                'Student Malus': df_list_student_malus,
                                'Total Malus': sum(Roster.complete_malus.values())})

    if visualize:
        # Current working directory
        current_dir = os.getcwd()

        # Parent directory
        parent_dir = os.path.dirname(current_dir)

        # Directory "visualize"
        visualize_directory = os.path.join(parent_dir, 'AH/visualize')

        # Export to excel file
        schedule_df.to_excel(f"{visualize_directory}/schedule.xlsx", index=False)

    return schedule_df