
# dict = {1:0, 2:0, 3:0}
# print(list(dict)[-1])
from functions.assign import *
course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)

# i = 0
# for student in student_list:
#     for course in student.courses:
#         if course.name == 'Autonomous Agents 2':
#             i += 1
# print(i)

# bio informatica 40 -> 45
# prog in java 2 95 -> 110
# netw en syst 50 -> 64
# aut agents 2 19 -> 22

for course in course_list:
    if course.practica > 1:
        print(f"more than one for {course.name}")


    # remove days that only occur once and calc malus
    # self.same_day()

    # def same_day(self):
    #     days = []
    #     count = {}
    #     for timeslot in self.timeslots:
    #         days.append(timeslot['day'])
    #     for day in days:
    #         if day in count:
    #             count[day] += 1
    #         else:
    #             count[day] = 1
  
    #     self.timeslots = [timeslot for timeslot in self.timeslots if count[timeslot['day']] > 1]