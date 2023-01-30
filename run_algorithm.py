import classes.algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS

import json

if __name__ == '__main__':
    with open('data/settings.json', 'r') as f:
        dictionary = json.load(f)

    capacity = dictionary['capacity']
    popular = dictionary['popular']
    popular_own_day = dictionary['popular_own_day']
    difficult_students = dictionary['difficult_students']
    annealing = dictionary['annealing']
    visualize = dictionary['visualize']
    core_arrangement = 'Class'


    G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS,\
    capacity, popular, popular_own_day, difficult_students, annealing, visualize, core_arrangement)

    if not visualize:
        G.optimize()