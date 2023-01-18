import classes.roster as RosterClass
import classes.baseline as BaselineClass
import functions.schedule_fill as schedule
import functions.assign  as assign
import functions.dataframes as dataframe
import classes.change as change
from data.data import COURSES, STUDENT_COURSES, ROOMS
import copy



def initialise():
    # create the lists
    course_list, student_list, rooms = assign.assign(COURSES, STUDENT_COURSES, ROOMS)

    # create a roster
    Roster = RosterClass.Roster(rooms)

    # # fill the roster
    schedule.schedule_fill(Roster, course_list)

    # Calculate costs of roster
    Roster.total_malus(student_list)

    # Create a dataframe and export to excel for visual representation
    df = dataframe.schedule_dataframe(Roster, student_list)

    # Save as malus points
    malus_points = Roster.malus_count

    return df, malus_points, course_list, student_list, rooms, Roster

def hill_climber(df, malus_points, course_list, student_list, rooms, Roster):

    # list with the original and the path of the improved roster objects
    roster_list = []

    # set best roster and malus score
    best_roster = Roster
    best_malus_score = best_roster.malus_count

    # append the original roster
    roster_list.append(best_roster)

    for i in range(300):

        # change the roster 50 times and calculate the maluspoints
        for j in range(50):
            current_roster = copy.deepcopy(best_roster)
            swapper = change.Change(df, course_list, student_list, current_roster)
            swapper.swap_lecture_empty_room()
            current_roster.total_malus(student_list)
            current_malus_points = current_roster.malus_count

            # if the malus points are lower then the previous lowest malus points set the best to the new object
            if best_malus_score > current_malus_points:
                best_roster = current_roster
                best_malus_score = current_malus_points
        
        # append the new best roster
        roster_list.append(best_roster)

if __name__ == '__main__':
    # baseline = BaselineClass.Baseline()
    # baseline.rearrange()

    df, malus_points, course_list, student_list, rooms, Roster = initialise()

    hill_climber(df, malus_points, course_list, student_list, rooms, Roster)