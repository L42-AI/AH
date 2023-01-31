import classes.algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS
import csv
import json
import pickle

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

    for _ in range(10):
        print(f'this will take hours, please do not turn off, iteration {_} out of 10')
        G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS,\
        capacity, popular, popular_own_day, difficult_students, annealing, visualize, core_arrangement)

        if not visualize:
            total_output, best_schedule = G.optimize()
            with open(f'data/schedule{_ + 1}', 'wb') as f:
                pickle.dump(best_schedule, f)

            with open('data/simulated_annealing_from_125_points', 'a', newline='') as f:
                writer = csv.writer(f)
                if _ == 0:
                    writer.writerow(['Iteration', 'Malus', 'list_duration_since_innit'])

                for i in range(len(total_output)):
                    writer.writerow([i, total_output[i][0], total_output[i][1]])