import classes.algorithms.generator as GeneratorClass

import classes.GUI.init_GUI as InitApp


from data.data import COURSES, STUDENT_COURSES, ROOMS

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

def main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT):
    if not CLIMBING:
        if not VISUALIZE_INIT:
            G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, climbing=CLIMBING)
        else:
            G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, climbing=CLIMBING, visualize=True)
    else:
        if not ANNEALING:
            G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, climbing=CLIMBING)
            G.optimize()
        else:
            G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, climbing=CLIMBING)
            G.optimize()

if __name__ == '__main__':
    # if profile:
    #     cProfile.run('main_runner(ANNEALING, CAPACITY)', 'profile.out')
    #     p = pstats.Stats('profile.out')
    #     p.strip_dirs().sort_stats('time').print_stats(100)
    # else:
    main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT)
    # App = InitApp.App()
    # App.run()
