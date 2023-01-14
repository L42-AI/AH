import classes.roster as RosterClass
import classes.baseline as BaselineClass
import functions.schedule_fill as schedule
import functions.assign  as assign
import functions.dataframes as dataframe

from data import COURSES, STUDENT_COURSES, ROOMS



def initialise():
    # create the lists
    course_list, student_list, rooms = assign.assign(COURSES, STUDENT_COURSES, ROOMS)

    # create a roster
    Roster = RosterClass.Roster(rooms)

    # fill the roster
    schedule.schedule_fill(Roster, course_list)

    # Calculate costs of roster
    Roster.total_malus(student_list)

    # Create a dataframe and export to excel for visual representation
    schedule_df = dataframe.schedule_dataframe(Roster, student_list)
    schedule_df.to_excel('Schedule.xlsx', index=False)

    # Save as malus points
    malus_points = Roster.malus

    return malus_points

if __name__ == '__main__':
    baseline = BaselineClass.Baseline()
    # baseline.plot_startup()
