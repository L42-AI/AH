from main import initialise
import os
import matplotlib.pyplot as plt
import numpy as np
import classes.change as ChangeClass
from tqdm import tqdm

class Baseline():
    def __init__(self, visualize=False):
        self.costs = []
        self.iterations = []
        self.df, self.malus, self.course_list, self.student_list, self.rooms, self.Roster = initialise()
        if visualize:
            self.plot_startup()

    def initialize(self, iters=1):
        for i in tqdm(range(iters)):
            self.costs.append(initialise()[1])
            self.iterations.append(i)

    def plot_startup(self):

        self.initialize(300)

        fig_name = "startups.png"

        # Current working directory
        current_dir = os.getcwd()

        # Parent directory
        parent_dir = os.path.dirname(current_dir)

        # Directory "visualize"
        directory_plots = os.path.join(parent_dir, 'AH/visualize')

        # Fit a polynomial of degree 1 (i.e. a linear regression) to the data
        coefficients = np.polyfit(self.iterations, self.costs, 1)

        # Create a new set of x values for the regression line
        x_reg = np.linspace(min(self.iterations), max(self.iterations), 300)

        # Use the coefficients to calculate the y values for the regression line
        y_reg = np.polyval(coefficients, x_reg)

        plt.title('300 random startups of the algorithm with no restrictions')
        plt.plot(self.iterations, self.costs)

        # Plot the regression line
        plt.plot(x_reg, y_reg, 'r')
        plt.xlabel('run #')
        plt.ylabel('malus points')
        plt.savefig(os.path.join(directory_plots, fig_name))
        plt.show()

    def get_schedule(self):
        return self.Roster.schedule

    def get_malus(self):
        return self.Roster.malus_count

    def get_malus_cause(self):
        return self.Roster.all_malus_cause

    def run(self, iters = 200):
        for i in tqdm(range(iters)):
            self.costs.append()
            self.iterations.append(i)

    def rearrange(self):
        Schuffeler = ChangeClass.Change(self.df, self.course_list, self.student_list, self.Roster)
        Schuffeler.swap_2_students(num=100)
        self.Roster.total_malus(self.student_list)
