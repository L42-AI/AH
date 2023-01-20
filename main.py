import classes.Algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS


import cProfile
import pstats

def main_runner():
    if __name__ == '__main__':

        # heuristics to allow for more random mutations before score calculation
        ANNEALING = False

        # heuristics to try and connect room size to class size 
        CAPACITY = True

        G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY)
        G.rearrange_HC()

cProfile.run('main_runner()', 'profile.out')
p = pstats.Stats('profile.out')
p.strip_dirs().sort_stats('time').print_stats(10)