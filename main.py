import classes.Algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS

import cProfile
import pstats

# Run profiler
profile = False

# heuristics to allow for more random mutations before score calculation
ANNEALING = True

# heuristics to try and connect room size to class size
CAPACITY = True

# heuristic to first give the popular classes rooms
POPULAR = True

# heuristic to place the most popular course lectures on different days
POPULAR_OWN_DAY = True


def main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY):
    stop = False
    if not ANNEALING:

        while stop == False:
            G = GeneratorClass.Generator_HC(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY)
            G.rearrange_HC()
    
    else:

        while stop == False:
            G = GeneratorClass.Generator_SA(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY)
            G.rearrange_HC()

if __name__ == '__main__':
    if profile:
        cProfile.run('main_runner(ANNEALING, CAPACITY)', 'profile.out')
        p = pstats.Stats('profile.out')
        p.strip_dirs().sort_stats('time').print_stats(100)
    else:
        main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY)