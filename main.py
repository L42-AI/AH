import classes.Algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS
import copy



if __name__ == '__main__':
    G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, visualize=False)
    print(G.Roster.malus_count)
    G.rearrange()
    print(G.Roster.malus_count)