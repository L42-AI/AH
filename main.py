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

    # for key in Roster.schedule:
    #     print(key)
    #     print(Roster.schedule[key])
    #     print("-----------------------")

    # Calculate costs of roster
    Roster.total_malus(student_list)

    # Create a dataframe and export to excel for visual representation
    df = dataframe.schedule_dataframe(Roster, student_list)

    # change.change_students(df, course_list, Roster)

    # Save as malus points
    malus_points = Roster.malus_count

    return df, malus_points, course_list, student_list, rooms, Roster

def swap_lecture(courses, course, students, roster):

    # pick a random course to swap with that is not the same as as the course and the new course does have lectures
    random_course = random.choice([c for c in courses if c != course and c.lectures > 0])

    # make a list of all the lectures
    lecture_switch = [key for key in roster.schedule[course.name].keys() if "lecture" in key]

    # if there are more then 1 lecture choose a random one
    if len(lecture_switch) > 1:
        lecture_switch = random.choice(lecture_switch)

    # else make from list string again
    else:
        lecture_switch = lecture_switch[0]

    # make a list of all the lectures for the random
    lecture_random = [key for key in roster.schedule[random_course.name].keys() if "lecture" in key]

    # if there are more then 1 lecture choose a random one
    if len(lecture_random) > 1:
        lecture_random = random.choice(lecture_random)

    else:
        lecture_random = lecture_random[0]

    # hard copy the dictionaries in order to switch the keys
    dict_switch = roster.schedule[course.name][lecture_switch].copy()
    dict_random = roster.schedule[random_course.name][lecture_random].copy()
    keys_to_switch = ['day', 'timeslot', 'room']

    # loop over the keys you want to switch and switch
    for key in keys_to_switch:
        roster.schedule[course.name][lecture_switch][key] = dict_random[key]
        roster.schedule[random_course.name][lecture_random][key] = dict_switch[key]



if __name__ == '__main__':
    baseline = BaselineClass.Baseline()
    print(baseline.malus)
    baseline.rearrange()


    # df, malus_points, courses, students, rooms, roster = initialise()

    # # print(courses[0].name)

    # swap_lecture(courses, courses[0], students, roster)

