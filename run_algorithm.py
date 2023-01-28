import classes.algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS

import json

def extract_json(dictionary):
    capacity = dictionary['capacity']
    popular = dictionary['popular']
    popular_own_day = dictionary['popular_own_day']
    hill_climbing = dictionary['hill_climbing']
    annealing = dictionary['annealing']
    visualize = dictionary['visualize']

    return capacity, popular, popular_own_day, hill_climbing, annealing, visualize

if __name__ == "__main__":

    with open('data/settings.json', 'r') as f:
        dictionary = json.load(f)

    capacity, popular, popular_own_day, hill_climbing, annealing, visualize = extract_json(dictionary)

    if not hill_climbing:
        visualize=True

    G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS,\
        capacity, popular, popular_own_day, visualize, annealing=annealing)
    G.optimize()