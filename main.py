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

def main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT):
    if not CLIMBING:
        if not VISUALIZE_INIT:
            G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, climbing=CLIMBING)
        else:
            G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, climbing=CLIMBING, visualize=True)
    else:
        pass
        # if not ANNEALING:
        #     G = GeneratorClass.Generator_HC(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, climbing=CLIMBING)
        #     G.optimize()
        # else:
        #     G = GeneratorClass.Generator_SA(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, climbing=CLIMBING)
        #     G.optimize()

if __name__ == '__main__':
    list_total_malus = []
    list_class_random = []
    list_class_capacity = []
    list_student_gaphour = []
    list_student_doublehour = []

    lists_to_append = [list_total_malus, list_class_random, list_class_capacity, list_student_gaphour, list_student_doublehour]


    if application:
        App = InitClass.App()
        App.run()
    else:

        # run the experiment 30 times
        for i in range(2):
            lists = main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT)

            for lst, list_to_append in zip(lists, lists_to_append):
                for value in lst:
                    list_to_append.append(value)
    
        data = {
            'Total Malus': list_total_malus,
            'Swap Class Random': list_class_random, 
            'Swap Class Capacity': list_class_capacity,
            'Swap Student Gaphour': list_student_gaphour,
            'Swap Student Doublehour': list_student_doublehour
            }

        df = pd.DataFrame(data)

        print(df)

        df.to_csv('data/Normal Hillclimber.csv')


