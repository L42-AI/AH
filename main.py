import classes.Algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS


if __name__ == '__main__':
    G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS, visualize=True)
    # G.rearrange()
