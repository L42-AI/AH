from classes import *
from data import *
from assign import *


course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

# THIS CAN PROBABLY BE DELETED LATER BUT IT IS NICE FOR OVERVIEW #
## first go over every course and see how many timeslots are needed
### timeslot needed for every lecture, tut, pract
time_slot_count = 0
for course in course_list:
    time_slot_count += course.lectures + course.tutorial_rooms + course.practica_rooms
# print(time_slot_count)

roster = Roster(rooms)
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

for key in roster.schedule:
    print(key)
    print(roster.schedule[key])
    print("---------------")