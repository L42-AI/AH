import classes.GUI.init_GUI as InitApp
import classes.algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS

computer = 'Jacob'
if __name__ == '__main__':

    if computer == 'Luka':
        for A in [True, False]:
            for B in [True, False]:
                for C in [True, False]:
                    for D in ['Class', 'Student', 'Mix']:
                        capacity = A
                        difficult_students = B
                        annealing = C
                        core_arrangement = D

                        visualize = False
                        popular = False
                        popular_own_day = False


                        G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS,\
                        capacity, popular, popular_own_day, difficult_students, annealing, visualize, core_arrangement)

                        G.optimize()

    # elif computer == 'Jacob':
        # for E in ['Mix']:
        #     capacity = True
        #     popular = True
        #     popular_own_day = True
        #     annealing = False
        #     core_arrangement = E

        #     difficult_students = False   
        #     visualize = False

        #     G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS,\
        #     capacity, popular, popular_own_day, difficult_students, annealing, visualize, core_arrangement)

        #     G.optimize()
        #     raise
    App = InitApp.App()
    App.run()