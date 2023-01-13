from classes.roster import *
from functions.schedule_fill import *
from functions.assign import *
from data import *
from classes.baseline import *

def main():
    # create the lists
    course_list, student_list, rooms = assign(COURSES, STUDENT_COURSES, ROOMS)

    # create a roster
    roster = Roster(rooms)

    # fill the roster
    schedule_fill(roster, course_list)
    roster.total_cost(student_list)

    # Calculate costs of roster
    roster.total_cost(student_list)

    # Save as malus points
    malus_points = roster.cost

    return malus_points

if __name__ == '__main__':
    baseline = Baseline(1000)
