import classes.Algorithms.hillclimber as HillCLimberClass
from multiprocessing import Pool

import copy
from tqdm import tqdm

class HCMultiprocessor():
    def __init__(self, Roster, course_list, student_list):
        self.Roster = Roster
        self.course_list = course_list
        self.student_list = student_list

    def run_hillclimbers(self):


        iter_counter = 0
        print(f'\nInitialization')
        print(self.Roster.malus_cause)
        while self.Roster.malus_cause['Dubble Classes'] != 0 or self.Roster.malus_cause['Capacity'] != 0:
        # while iter_counter != 1:
            iter_counter += 1

            # Make four deepcopys for each function to use
            self.rosters = [copy.deepcopy(self.Roster) for _ in range(4)]

            # Fill the pool with all functions and their copied rosters
            with Pool(4) as p:
                output_rosters = p.map(self.run_HC, [(1, self.rosters[0]), (2, self.rosters[1]), (3, self.rosters[2]), (4, self.rosters[3])])

            # find the lowest malus of the output rosters
            min_malus = min([i.malus_count for i in output_rosters])

            # Use the lowest malus to find the index of the best roster
            best_index = [i.malus_count for i in output_rosters].index(min_malus)

            # If the new roster is smaller than the current roster:
            if output_rosters[best_index].malus_count < self.Roster.malus_count:

                # Set the new roster to self.Roster
                self.Roster = output_rosters[best_index]

                print(f'\nGeneration: {iter_counter}')
                print(f'Most effective function: HC{best_index + 1}')
                print(self.Roster.malus_cause)
            else:
                print('\nUnsuccesfull:')
                print(f'Generation: {iter_counter}')
                print(self.Roster.malus_cause)


    def run_HC(self, hc_tuple):
        number, roster = hc_tuple
        if number == 1:
            # print('looking to swap classes...')
            HC1 = HillCLimberClass.HC_LectureSwap(roster, self.course_list, self.student_list)
            roster = HC1.climb()
            # print(f'HC1: {roster.malus_count}')
            return roster

        elif number == 2:
            # print('looking to swap students randomly...')
            HC2 = HillCLimberClass.HC_StudentSwap(roster, self.course_list, self.student_list)
            roster = HC2.climb()
            # print(f'HC2: {roster.malus_count}')
            return roster

        elif number == 3:
            # print('looking to swap students on gap hour malus...')
            HC3 = HillCLimberClass.HC_SwapBadTimeslots_GapHour(roster, self.course_list, self.student_list)
            roster = HC3.climb()
            # print(f'HC3: {roster.malus_count}')
            return roster

        elif number == 4:
            # print('looking to swap students on double classes malus...')
            HC4 = HillCLimberClass.HC_SwapBadTimeslots_DoubleClasses(roster, self.course_list, self.student_list)
            roster = HC4.climb()
            # print(f'HC4: {roster.malus_count}')
            return roster
