from classes import *
from data import *
from assign import *


course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

# create a roster
roster = Roster(rooms)

# fill the roster
for course in course_list:
    class_count = 0
    for i in range(course.lectures):
        roster.fill_schedule(course, "lecture", class_count, i + 1)
        class_count += 1
    for i in range(course.tutorial_rooms):
        roster.fill_schedule(course, "tutorials", class_count, i + 1)
        class_count += 1
    for i in range(course.practica_rooms):
        roster.fill_schedule(course, "practica", class_count, i + 1)
        class_count += 1

# output
for key in roster.schedule:
    print("------------------------")
    print(key)
    print("------------------------")
    print(roster.schedule[key])
    print()
    

# # check if students get group
# for student in student_list:
#     print(student.tut_group, student.pract_group)
#     break

## timeslot needed for every lecture, tut, pract
# time_slot_count = 0
# for course in course_list:
#     time_slot_count += course.lectures + course.tutorial_rooms + course.practica_rooms
#  print(time_slot_count)