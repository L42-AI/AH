import classes.algorithms.generator as GeneratorClass
import classes.GUI.Init as InitClass

from data.data import COURSES, STUDENT_COURSES, ROOMS
import pandas as pd
import cProfile
import pstats
import csv

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

def write_to_csv( save_location, iteration, list_iterations, list_total_malus, list_class_random, list_class_capacity, list_student_gaphour, list_student_doublehour, list_duration_since_innit):
    with open(save_location, 'a', newline='') as f:
        writer = csv.writer(f)
        if iteration == 0:
            writer.writerow(['Iteration', 'list_iterations', 'Iteration', 'Swap Class Random', 'Swap Class Capacity', 'Swap Student Gaphour', 'Swap Student Doublehour', 'list_duration_since_innit'])

        for i in range(len(list_iterations)):
            writer.writerow([iteration, list_iterations[i], list_total_malus[i], list_class_random[i], list_class_capacity[i], list_student_gaphour[i], list_student_doublehour[i], list_duration_since_innit[i]])

def main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT, multiplier=0.1):

    G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, capacity=CAPACITY, popular=POPULAR, popular_own_day=POPULAR_OWN_DAY, difficult_students=DIFICULT_STUDENTS, multiplier=multiplier)

    return G.optimize()


if __name__ == '__main__':

    multiplier = 4

    for i in range(26, 30):
        list_iterations, list_total_malus, list_class_random, list_class_capacity, list_student_gaphour, list_student_doublehour, list_duration_since_innit = main_runner(ANNEALING, CAPACITY, POPULAR, POPULAR_OWN_DAY, CLIMBING, VISUALIZE_INIT, multiplier=multiplier)
        write_to_csv('data/One Hillclimber stages multiplier_4.csv', i, list_iterations, list_total_malus, list_class_random, list_class_capacity, list_student_gaphour, list_student_doublehour, list_duration_since_innit)

