import classes.roster as RosterClass
import classes.baseline as BaselineClass
import functions.schedule_fill as schedule
import functions.assign  as assign


from data import COURSES, STUDENT_COURSES, ROOMS



def initialise():
    # create the lists
    course_list, student_list, rooms = assign.assign(COURSES, STUDENT_COURSES, ROOMS)

    # create a roster
    roster = RosterClass.Roster(rooms)

    # fill the roster
    schedule.schedule_fill(roster, course_list)

    # Calculate costs of roster
    roster.total_cost(student_list)

    # Save as malus points
    malus_points = roster.cost

    return malus_points

if __name__ == '__main__':
    BaselineClass.Baseline(iters=300)
