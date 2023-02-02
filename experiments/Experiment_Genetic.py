import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


if __name__ == '__main__':

    # load the csv into a dataframe
    df = pd.read_csv(r'data/experiment5.csv')

    # get the lowest malus and their itirations
    minimum_y = df['Cost'].min()
    minimum_x = df[df['Cost'] == minimum_y].index[0]

    plt.figure(figsize=(10,4))
    plt.style.use('seaborn-whitegrid')

    # plot the data
    sns.lineplot(data=df, x=df.index, y='Cost')

    plt.scatter(minimum_x, minimum_y, c='green')
    plt.annotate(f'Minimum: {minimum_y}', (minimum_x + 40, minimum_y - 2), textcoords='offset points', xytext=(-15,10), ha='center', color='green', fontsize=12)

    plt.title('Genetic')

    plt.xlabel('Iteration')
    plt.ylabel('Malus')

    plt.savefig(r'plots/Genetic.png', dpi=1000)

    plt.show()