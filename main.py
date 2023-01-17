import classes.roster as RosterClass
import classes.baseline as BaselineClass
import functions.schedule_fill as schedule
import functions.assign  as assign
import functions.dataframes as dataframe
import functions.change_students as change
import random

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
    df = dataframe.schedule_dataframe(Roster, student_list)

    # Save as malus points
    malus_points = Roster.malus_count

    return malus_points, course_list, student_list, rooms, Roster

def swap_lecture(courses, course, students, roster):
    
    # pick a random course to swap with that is not the same as as the course and the new course does have lectures
    random_course = random.choice([c for c in courses if c != course and c.lectures > 0])

    # make a list of all the lectures
    lecture_switch = [key for key in roster.schedule[course.name].keys() if "lecture" in key]
    lecture_random = [key for key in roster.schedule[random_course.name].keys() if "lecture" in key]

    # take a random one (if only one it will take the one)
    lecture_switch = random.choice(lecture_switch)
    lecture_random = random.choice(lecture_random)

    # hard copy the dictionaries in order to switch the keys
    dict_switch = roster.schedule[course.name][lecture_switch]
    dict_random = roster.schedule[random_course.name][lecture_random]

    # switch the times in the schedule roster
    roster.schedule[course.name][lecture_switch] = dict(zip(dict_switch, dict_random.values()))
    roster.schedule[random_course.name][lecture_random] = dict(zip(dict_random, dict_switch.values()))

if __name__ == '__main__':
    # baseline = BaselineClass.Baseline()
    # baseline.plot_startup()

    malus_points, courses, students, rooms, roster = initialise()

    # print(courses[0].name)

    swap_lecture(courses, courses[0], students, roster)

