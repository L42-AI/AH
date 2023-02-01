import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import pandas as pd


if __name__ == '__main__':

    df = pd.read_csv('One Hillclimber different stages multiplier_4.csv')

    list_malus = []
    list_max_iterations = []

    minimum_y = df['Iteration.1'].min()
    minimum_x = df[df['Iteration.1'] == minimum_y].index[0]

    split_indices = np.where(df['list_iterations'] == 0)[0]
    dfs = np.split(df, split_indices)

    for i, d in enumerate(dfs):
        if i != 0:
            list_max_iterations.append(d['list_iterations'].max())
            list_malus.append(d['Iteration.1'].min())

    average_iterations = statistics.mean(list_max_iterations)
    average_malus = statistics.mean(list_malus)

    # print(f'Average iterations is: {average_iterations}')
    sns.lineplot(data=df, x=df.index, y='Iteration.1')

    plt.scatter(minimum_x, minimum_y, c='green')
    plt.annotate(f'Minimum: {minimum_y}', (minimum_x, minimum_y - 80), textcoords='offset points', xytext=(-15,10), ha='center', color='green', fontsize=12)

    plt.axhline(y=average_malus, color='red', linestyle='--')
    plt.text(0, average_malus - 50, f'Average Malus: {average_malus}', color='red', fontsize=12, ha='left', va='center')

    plt.text(30, 1700, f'Average Generations: {average_iterations}', color='black', fontsize=12, ha='left', va='center')
    plt.text(30, 1750, f'Iterations per Generations: 50', color='black', fontsize=12, ha='left', va='center')

    plt.xlabel('Iteration')
    plt.ylabel('Malus')
    plt.title('Experiment Hillclimber Multiplier 4', fontsize=20)

    plt.savefig('Plot Hillclimber Multiplier 4.png', dpi=1000)

    fig = plt.gcf()
    fig.set_size_inches((12, 12), forward=False)
    fig.savefig('Plot Hillclimber Multiplier 4.png', dpi=1000)

    plt.show()