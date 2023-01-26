import classes.Algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS

import cProfile
import pstats

# Run profiler
profile = False

# heuristics to allow for more random mutations before score calculation
ANNEALING = False

# heuristics to try and connect room size to class size
CAPACITY = True

<<<<<<< HEAD
# heuristic to first give the popular classes rooms
POPULAR = True

# heuristic to place the most popular course lectures on different days
POPULAR_OWN_DAY = True
=======

>>>>>>> 87c0c378b6d20d092dec819fd304d57f4fe767c2

def main_runner(ANNEALING, CAPACITY):
    stop = False
    while stop == False:
        G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY)
        G.rearrange_HC()

if __name__ == '__main__':
    if profile:
        cProfile.run('main_runner(ANNEALING, CAPACITY)', 'profile.out')
        p = pstats.Stats('profile.out')
        p.strip_dirs().sort_stats('time').print_stats(100)
    else:
        main_runner(ANNEALING, CAPACITY)