import classes.Algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS
import copy



if __name__ == '__main__':
    G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS)
    # print(G.get_schedule()['No course'])

    G.rearrange()

    # print(G.get_schedule()['No course'])

