from classes.roster import *
from functions.schedule_fill import *
from functions.assign import *
from data import *
import matplotlib.pyplot as plt

def initialize_random_state(roster, course_list, student_list, malus_points):

    # fill the roster
    schedule_fill(roster, course_list)
    roster.total_cost(student_list)

    malus_points.append(roster.cost)

    roster.total_cost(student_list)
    return

list_std = []
list_course = []
list_room = []
malus_points = []
run = []
roster = []

for i in range(10):

    std = "student" + str(i)
    course = "course" + str(i)
    rooms = "course" + str(i)

    # create the lists
    course, std, rooms = assign(COURSES, STUDENT_COURSES, ROOMS)

    # put the new object lists in the list
    list_std.append(std)
    list_course.append(course)
    list_room.append(rooms)

    run.append(i)
    # create a roster
    roster.append(Roster(rooms))

    # run model on new objects
    initialize_random_state(roster[i], list_course[i], list_std[i], malus_points)

plt.plot(run, malus_points)
plt.show()