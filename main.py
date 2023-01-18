import classes.roster as RosterClass
import classes.baseline as BaselineClass
import functions.schedule_fill as schedule
import functions.assign  as assign
import functions.dataframes as dataframe
from classes.change import Change
import copy

from data.data import COURSES, STUDENT_COURSES, ROOMS



def initialise():
    # create the lists
    course_list, student_list, rooms = assign.assign(COURSES, STUDENT_COURSES, ROOMS)

    # create a roster
    Roster = RosterClass.Roster(rooms)

    # # fill the roster
    schedule.schedule_fill(Roster, course_list)
    # for key in Roster.schedule:
    #     print(key)
    #     print(Roster.schedule[key])
    #     print("-----------------------")

    # Calculate costs of roster
    Roster.total_malus(student_list)

    # Create a dataframe and export to excel for visual representation
    df = dataframe.schedule_dataframe(Roster, student_list)

    # Save as malus points
    malus_points = Roster.malus_count

    return malus_points, course_list, student_list, rooms, Roster

def hill_climber(malus_points, courses, students, rooms, Roster):

    list_copies = []
    # list_functions = [change.switch_2_students, change.swap_2_lectures, change.swap_lecture_empty_room  ]
    print(Roster.schedule)
    swapper = Change()
    swapper.swap_lecture_empty_room()

    # for i in range(50):
    #     roster
    #     list_copies.append(copy.deepcopy(roster))


if __name__ == '__main__':
    # baseline = BaselineClass.Baseline()
    # baseline.plot_startup()

    malus_points, courses, students, rooms, Roster = initialise()

    
    hill_climber(malus_points, courses, students, rooms, Roster)