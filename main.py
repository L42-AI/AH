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

# heuristic to first give the popular classes rooms
POPULAR = False

# heuristic to place the most popular course lectures on different days
POPULAR_OWN_DAY = False


def main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY):
    if not ANNEALING:
        for a in [True, False]:
            for b in [True, False]:
                for c in [True, False]:
                    G = GeneratorClass.Generator_HC(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=a, popular=b, popular_own_day=c)
                    G.rearrange_HC(a, b, c)

    else:
        G = GeneratorClass.Generator_SA(COURSES, STUDENT_COURSES, ROOMS, annealing=ANNEALING, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY)
        G.rearrange_HC()
        G.create_dataframe(G.Roster, G.student_list, visualize=True)

if __name__ == '__main__':
    if profile:
        cProfile.run('main_runner(ANNEALING, CAPACITY)', 'profile.out')
        p = pstats.Stats('profile.out')
        p.strip_dirs().sort_stats('time').print_stats(100)
    else:
        main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY)