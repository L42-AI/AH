from classes import *
from data import *
from assign import *

course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

# create a roster
roster = Roster(rooms)

# fill the roster
for course in course_list:

    # go over the number of lectures, tutorials and practicals needed
    for i in range(course.lectures):

        # check how many students will attend this lecture
        attending = course.expected
        roster.fill_schedule(course, "lecture", i + 1, attending)

    for i in range(course.tutorial_rooms):

        # check how many students will attend this tutorial
        attending = course.tut_group_dict[i + 1]
        roster.fill_schedule(course, "tutorials", i + 1, attending)

    for i in range(course.practica_rooms):

        # check how many students will attend this practical
        attending = course.pract_group_dict[i + 1]
        roster.fill_schedule(course, "practica", i + 1, attending)


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
