from main import initialise
import os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

class Baseline():
    def __init__(self, iters=2):
        self.costs = []
        self.iterations = []
        self.run(iters)


    def run(self, iters):
        for i in tqdm(range(iters)):
            self.costs.append(initialise())
            self.iterations.append(i)

    def plot_startup(self):

        fig_name = "startups.png"

        # Current working directory
        current_dir = os.getcwd()

        # Parent directory
        parent_dir = os.path.dirname(current_dir)

        # Directory "plots"
        directory_plots = os.path.join(parent_dir, 'AH/plots')

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
        # plt.savefig(os.path.join(directory_plots, fig_name))
        plt.show()


