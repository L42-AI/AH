
# dict = {1:0, 2:0, 3:0}
# print(list(dict)[-1])
from assign import *
course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

i = 0
for student in student_list:
    for course in student.courses:
        if course.name == 'Autonomous Agents 2':
            i += 1
print(i)

# bio informatica 40 -> 45
# prog in java 2 95 -> 110
# netw en syst 50 -> 64
# aut agents 2 19 -> 22