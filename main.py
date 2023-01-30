import classes.algorithms.generator as GeneratorClass
import classes.GUI.Init as InitClass

from data.data import COURSES, STUDENT_COURSES, ROOMS
import pandas as pd
import cProfile
import pstats

# Run profiler
profile = False

# Heuristic to employ Hill climbing algorithm
CLIMBING = True

# heuristics to allow for more random mutations before score calculation
ANNEALING = False

# heuristics to try and connect room size to class size
CAPACITY = False

# heuristic to first give the popular classes rooms
POPULAR = False

# heuristic to place the most popular course lectures on different days
POPULAR_OWN_DAY = False

VISUALIZE_INIT = True

# application or not
application = False

DIFICULT_STUDENTS = False

def main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT, multiplier=0.1):

    G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, difficult_students=DIFICULT_STUDENTS, multiplier=multiplier)

    return G.optimize()


if __name__ == '__main__':
    # list_iterations = []
    # list_total_malus = []
    # list_class_random = []
    # list_class_capacity = []
    # list_student_gaphour = []
    # list_student_doublehour = []

    # lists_to_append = [list_iterations, list_total_malus, list_class_random, list_class_capacity, list_student_gaphour, list_student_doublehour]

    # # run the experiment 30 times
    # for i in range(30):
    #     lists = main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT)

    #     for lst, list_to_append in zip(lists, lists_to_append):
    #         for word in lst:
    #             list_to_append.append(word)

    # data = {
    #     'Iteration': list_iterations,
    #     'Total Malus': list_total_malus,
    #     'Swap Class Random': list_class_random, 
    #     'Swap Class Capacity': list_class_capacity,
    #     'Swap Student Gaphour': list_student_gaphour,
    #     'Swap Student Doublehour': list_student_doublehour
    #     }

    # df = pd.DataFrame(data)

    # print(df)

    # df.to_csv('data/Normal Hillclimber geen multiplier 30 keer.csv')

    list_multipliers = [0.1, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    list_iterations = []
    list_total_malus = []
    list_class_random = []
    list_class_capacity = []
    list_student_gaphour = []
    list_student_doublehour = []
    list_duration_since_innit = []

    lists_to_append = [list_iterations, list_total_malus, list_class_random, list_class_capacity, list_student_gaphour, list_student_doublehour, list_duration_since_innit]

    for multiplier in list_multipliers:

        lists = main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT, multiplier)

        for lst, list_to_append in zip(lists, lists_to_append):
            for word in lst:
                list_to_append.append(word)

    data = {
        'List Iterations': list_iterations,
        'Duration since innit': list_duration_since_innit,
        'Total Malus': list_total_malus,
        'Swap Class Random': list_class_random, 
        'Swap Class Capacity': list_class_capacity,
        'Swap Student Gaphour': list_student_gaphour,
        'Swap Student Doublehour': list_student_doublehour
        }

    df = pd.DataFrame(data)

    df.to_csv('data/Different Multipliers.csv')


    print(df)

    # main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT)