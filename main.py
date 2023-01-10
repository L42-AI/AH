from classes import *
from data import *
from assign import *

'''
**UPLOADEN**
git add main.py
git commit -m "nieuwe main" 
git push origin Jacob
'''

course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

# THIS CAN PROBABLY BE DELETED LATER BUT IT IS NICE FOR OVERVIEW #
## first go over every course and see how many timeslots are needed
### timeslot needed for every lecture, tut, pract
time_slot_count = 0
for course in course_list:
    time_slot_count += course.lectures + course.tutorials + course.practica
print(time_slot_count)

roster = Roster(rooms)
for course in course_list:
    roster.fill_schedule(course)