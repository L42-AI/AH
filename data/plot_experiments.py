import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import pandas as pd


def visualize_experiments(file_location, save_location, title, iteration_name, malus_name, location_generations, location_iterations, location_minimum, location_average):
    df = pd.read_csv(file_location)

    list_malus = []
    list_max_iterations = []

    minimum_y = df[malus_name].min()
    minimum_x = df[df[malus_name] == minimum_y].index[0]

    split_indices = np.where(df[iteration_name] == 0)[0]
    dfs = np.split(df, split_indices)

    for i, d in enumerate(dfs):
        if i != 0:
            list_max_iterations.append(d[iteration_name].max())
            list_malus.append(d[malus_name].min())

    average_iterations = statistics.mean(list_max_iterations)
    average_malus = statistics.mean(list_malus)

    # print(f'Average iterations is: {average_iterations}')
    sns.lineplot(data=df, x=df.index, y=malus_name)

    plt.scatter(minimum_x, minimum_y, c='green')
    plt.annotate(f'Minimum: {minimum_y}', (minimum_x, minimum_y - location_minimum), textcoords='offset points', xytext=(-15,10), ha='center', color='green', fontsize=12)

    plt.axhline(y=average_malus, color='red', linestyle='--')
    plt.text(0, average_malus - location_average, f'Average Malus: {average_malus}', color='red', fontsize=12, ha='left', va='center')

    plt.text(30, location_generations, f'Average Generations: {average_iterations}', color='black', fontsize=12, ha='left', va='center')
    plt.text(30, location_iterations, f'Iterations per Generations: 50', color='black', fontsize=12, ha='left', va='center')

    plt.xlabel('Iteration')
    plt.ylabel('Malus')
    plt.title(title, fontsize=20)

    plt.savefig(save_location, dpi=1000)

    fig = plt.gcf()
    fig.set_size_inches((12, 12), forward=False)
    fig.savefig(save_location, dpi=1000)

    plt.show()


if __name__ == '__main__':

    visualize_experiments('One Hillclimber different stages multiplier_4.csv', 'Plot Hillclimber Multiplier 4.png', 'Experiment Hillclimber Multiplier 4', \
    'list_iterations' ,'Iteration.1', 1700, 1750, 80, 50)