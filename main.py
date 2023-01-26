import classes.Algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cProfile
import pstats
from data.store_data import store_improvements

# Run profiler
profile = False

# heuristics to allow for more random mutations before score calculation
ANNEALING = False

# heuristics to try and connect room size to class size
CAPACITY = False



def main_runner(ANNEALING, CAPACITY):
    # stop = False
    # while stop == False:
    G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY)
    swap_lecture, swap_student, swap_gaphour, swap_doublehours = G.rearrange_HC()
    
    store_improvements(swap_lecture, swap_student, swap_gaphour, swap_doublehours)


if __name__ == '__main__':
    if profile:
        cProfile.run('main_runner(ANNEALING, CAPACITY)', 'profile.out')
        p = pstats.Stats('profile.out')
        p.strip_dirs().sort_stats('time').print_stats(100)
    else:
        main_runner(ANNEALING, CAPACITY)