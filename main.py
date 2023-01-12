from classes.roster import *
from functions.schedule_fill import *
from functions.assign import *
from data import *

# create the lists
course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

# create a roster
roster = Roster(rooms)

# fill the roster
schedule_fill(roster, course_list)

# # output
# for key in roster.schedule:
#     print("------------------------")
#     print(key)
#     print("------------------------")
#     print(roster.schedule[key])
#     print()

roster.total_cost(student_list)


# # check if students get group
# for student in student_list:
#     print(student.tut_group, student.pract_group)
#     break

## timeslot needed for every lecture, tut, pract
# time_slot_count = 0
# for course in course_list:
#     time_slot_count += course.lectures + course.tutorial_rooms + course.practica_rooms
#  print(time_slot_count)
