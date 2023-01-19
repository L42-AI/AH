import classes.Algorithms.mutate as MutateClass

import copy

class HillClimber():
    def __init__(self, malus_points, Roster, df, course_list, student_list, room_list):
        self.roster_list = []
        pass

    def set_roster(self, Roster):
        # set best roster and malus score
        best_roster = Roster
        best_malus_score = best_roster.malus_count

        # append the original roster
        self.roster_list.append(best_roster)


def hill_climber(df, malus_points, course_list, student_list, rooms, Roster):

    # list with the original and the path of the improved roster objects
    roster_list = []

    # set best roster and malus score
    best_roster = Roster
    best_malus_score = best_roster.malus_count

    # append the original roster
    roster_list.append(best_roster)

    # list with all the different changes we want to use
    # list_changes = [swap_lecture_empty_room, swap_2_lectures, swap_2_students]

    for i in range(300):

        # make 50 changes to the roster
        for j in range(50):

            # make a deep copy, initiate the swapper with the right roster and change that roster
            current_roster = copy.deepcopy(best_roster)
            M = MutateClass.Mutate(df, course_list, student_list, current_roster)
            M.swap_lecture_empty_room()

            # calculate the maluspoints
            current_roster.total_malus(student_list)
            current_malus_points = current_roster.malus_count

            # if the malus points are lower then the previous lowest malus points set the best to the new object
            if best_malus_score > current_malus_points:
                best_roster = current_roster
                best_malus_score = current_malus_points

        # append the new best roster
        roster_list.append(best_roster)
        print(best_malus_score)

if __name__ == '__main__':
    hill_climber(df, malus_points, course_list, student_list, rooms, Roster)