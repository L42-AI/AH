import classes.Algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS

import cProfile
import pstats

# Run profiler
profile = False

# heuristics to allow for more random mutations before score calculation
ANNEALING = False

# heuristics to try and connect room size to class size
CAPACITY = False



def main_runner(ANNEALING, CAPACITY):
    stop = False
    while stop == False:
        G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY)
        G.rearrange_HC(visualize=True)

if __name__ == '__main__':
    if profile:
        cProfile.run('main_runner(ANNEALING, CAPACITY)', 'profile.out')
        p = pstats.Stats('profile.out')
        p.strip_dirs().sort_stats('time').print_stats(100)
    else:
        main_runner(ANNEALING, CAPACITY)