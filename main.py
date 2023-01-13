import classes.roster as roster
import functions.schedule_fill as schedule
import functions.assign 
from data import *
from classes.baseline import *


def main():
    # create the lists
    course_list, student_list, rooms = assign(COURSES, STUDENT_COURSES, ROOMS)

    # create a roster
    roster = roster.Roster(rooms)

    # fill the roster
    schedule.schedule_fill(roster, course_list)

    # Calculate costs of roster
    roster.total_cost(student_list)

    # Save as malus points
    malus_points = roster.cost

    return malus_points

if __name__ == '__main__':
    print(main())
