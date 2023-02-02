"""
This file contains the class hillclimber and all the classes that inherit this class
"""

import classes.representation.malus_calc as MalusCalculatorClass
import classes.algorithms.mutate as MutateClass
from data.assign import student_list, course_list

import numpy as np
import decimal
import random

""" Main HillClimber Class """

class HillClimber:
    '''
    This class is the framework for all hillclimbers. It is designed to be inherited
    by other Hillclimbers to perform one specific task. These tasks can be the following:
    - Swapping two random chosen seminars from two courses
    - Swapping one seminar that is causing the most capacity problems with a random seminar
    - Swapping one student to different tutorial group based on the group that is causing the most gap hours
    - Swapping one student to different tutorial group based on the group that is causing the most double hours
    '''

    def __init__(self, schedule, iteration=0):
        self.course_list = course_list
        self.student_list = student_list
        self.schedule = schedule
        self.iteration = iteration

        self.MC = MalusCalculatorClass.MC()

        # Compute malus with MalusCalculator
        self.malus = self.get_malus(self.schedule)

    """ Inheritable methods """

    def step_method(self, M):
        """
        Defines the step method
        """
        pass

    def get_name(self):
        """
        Get the name of the method used
        """
        pass

    def make_mutate(self, schedule):
        """
        Initiate mutate class
        """
        M = MutateClass.Mutate(schedule)
        return M

    def get_malus(self, schedule):
        """
        Return the score of the current schedule
        """
        return self.MC.compute_total_malus(schedule)

    """ Main Method """

    def climb(self, hill_climber_iters=400, T=0, ANNEALING=False, fail_counter=None):
        '''
        this method is the 'core' of every optimize algorithm. It performs a random mutation by calling
        a case specific mutate method and compares the schedule that mutation created to the current one
        the amount of iterations it makes before returning to the optimize script to compare results with
        other Hillclimbers is dependent on hill_climber_iters
        '''

        # Set boolean
        self.accept_me = False

        # Compute malus with function
        self.malus = self.get_malus(self.schedule)

        # set the number of iterations depending on user input
        if type(hill_climber_iters) == float:
            multiplier = True
            self.hill_climber_iters = int(self.malus['Total'] * hill_climber_iters)
        else:
            multiplier = False
            self.hill_climber_iters = hill_climber_iters

        # let the hillclimber take some steps
        for _ in range(self.hill_climber_iters):

            # Make copy of schedule, complex because of dictionary
            copied_schedule = self.recursive_copy(self.schedule)

            # Create the mutate class
            M = self.make_mutate(copied_schedule)

            # Take a step
            self.step_method(M)

            # Create a new variable to store the new schedule
            new_schedule = M.schedule

            # Calculate the malus points for the new schedule
            new_malus = self.get_malus(new_schedule)

            # let the hillclimber make 3 changes before a new score is calculated
            self.__accept_schedule(new_malus, new_schedule, T=T, ANNEALING=ANNEALING, fail_counter=fail_counter)

            self.iteration += 1

            # If multipier
            if multiplier:

                # Set hill climber iterations
                self.hill_climber_iters = int(self.malus['Total'] * hill_climber_iters)

        return self.schedule, self.malus, self.iteration, self.accept_me

    def __accept_schedule(self, new_malus, new_schedule, T=0, ANNEALING=False, fail_counter=None):
        '''
        Takes in the new malus (dict) and schedule (dict) and compares it to the current version
        If it is better, it will update the self.schedule and malus
        '''

        prob = random.random()
        # only accept annealing if the rise in malus is not too large
        difference = self.malus['Total'] - new_malus['Total']

        # only accept annealing if the rise in malus is not too large
        difference = self.malus['Total'] - new_malus['Total']
        prob = random.random()

        # create an accept threshold when using simulated annealing
        if new_malus['Total'] < 120 and ANNEALING and not self.accept_me and fail_counter > 500:
            accept = decimal.Decimal(1 - np.exp(-difference/T))
        else:
            accept = 2 # 2 can never be accepted

        # Compare with prior malus points
        if new_malus['Total'] <= self.malus['Total']:
            self.schedule = new_schedule
            self.malus = new_malus

        # do not accept worsenings that are too large
        elif prob > accept and difference < 20:
            T = 0
            # print(f'worsening of {-difference} got accepted at T: {T}')
            self.schedule = new_schedule
            self.malus = new_malus
            self.accept_me = True

    def recursive_copy(self, obj):
        """
        This method that makes a copy of our schedule that does not change the schedule
        when we modify the copy. This eliminates the need for deepcopy
        """

        # if instance is a dict
        if isinstance(obj, dict):

            # return object comprehension with recursive function call
            return {k: self.recursive_copy(v) for k, v in obj.items()}

        # if instance is a set
        elif isinstance(obj, set):

            # return object comprehension with recursive function call
            return {self.recursive_copy(x) for x in obj}
        else:
            # final return
            return obj

""" Inherited HillClimber Classes """

class SeminarSwapRandom(HillClimber):
    """
    This method swaps a random class with another random class
    """
    def step_method(self, M):
        """
        Defines the step method
        """
        # Take a random state to pass to function
        state = random.choice((True, False))
        M.swap_random_seminars(state)

    def get_name(self):
        """
        This method gets the name of the method used
        """
        return "SeminarSwapRandom"

class SeminarSwapCapacity(SeminarSwapRandom):
    """ This class swaps the seminar that has the most capacity malus points with a random other seminar """
    
    def make_mutate(self, schedule):
        """
        Initiates the mutate class
        """
        M = MutateClass.Mutate_Course_Swap_Capacity(schedule)
        return M

    def get_name(self):
        """
        Get the name of the method used
        """
        return "SeminarSwapCapacity"

class StudentSwapGapHour(HillClimber):
    """ This class takes a random student and finds the day with the most gap hours.
       When found, it will swap one tut or pract with a student from a different group
       that has the most malus points from that group """

    def step_method(self, M):
        """
        Defines the step method
        """
        M.swap_bad_timeslots()

    def get_name(self):
        """
        Get the name of the method used
        """
        return 'StudentSwapGapHour'

class StudentSwapDoubleHour(HillClimber):
    """
    This class takes a random student and finds the day with the most double classes.
    When found, it will swap one tut or pract with a student from a different group
    that has the most malus points from that group
    """

    def make_mutate(self, schedule):
        """
        Initiate mutate class
        """
        M = MutateClass.Mutate_double_classes(schedule)
        return M

    def step_method(self, M):
        """
        Defines the step method
        """
        M.swap_bad_timeslots()

    def get_name(self):
        """
        Get the name of the method used
        """
        return 'StudentSwapDoubleClasses'