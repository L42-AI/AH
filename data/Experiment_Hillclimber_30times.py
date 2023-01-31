import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import pandas as pd


if __name__ == '__main__':

    df = pd.read_csv('Normal Hillclimber geen multiplier 30 keer.csv')

    list_malus = []
    list_max_iterations = []

    minimum_y = df['Total Malus'].min()
    minimum_x = df[df['Total Malus'] == minimum_y].index[0]

    split_indices = np.where(df['Iteration'] == 0)[0]
    dfs = np.split(df, split_indices)

    for i, d in enumerate(dfs):
        if i != 0:
            list_max_iterations.append(d['Iteration'].max())
            list_malus.append(d['Total Malus'].min())

    average_iterations = statistics.mean(list_max_iterations)
    average_malus = statistics.mean(list_malus)

    sns.lineplot(data=df, x=df.index, y='Total Malus')

    plt.scatter(minimum_x, minimum_y, c='green')
    plt.annotate(f'Minimum: {minimum_y}', (minimum_x, minimum_y - 60), textcoords='offset points', xytext=(0,10), ha='center', color='green', fontsize=12)

    plt.axhline(y=average_malus, color='red', linestyle='--')
    plt.text(0, average_malus - 50, f'Average Malus: {average_malus}', color='red', fontsize=12, ha='left', va='center')

    plt.text(30, 1500, f'Average Generations: {average_iterations}', color='black', fontsize=12, ha='left', va='center')
    plt.text(30, 1550, f'Iterations per Generations: 50', color='black', fontsize=12, ha='left', va='center')

    plt.xlabel('Iteration')
    plt.ylabel('Malus')
    plt.title('Running Hillclimber 30 times', fontsize=20)

    plt.savefig('Plot Hillclimber 30 times.png', dpi=1000)

    fig = plt.gcf()
    fig.set_size_inches((14, 12), forward=False)
    fig.savefig('Plot Hillclimber 30 times.png', dpi=1000)

    plt.show()