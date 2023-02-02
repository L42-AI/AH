import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


if __name__ == '__main__':

    # load the csv into a dataframe
    df = pd.read_csv('experiment0.csv')

    # get the lowest malus and their itirations
    minimum_y = df['Cost'].min()
    minimum_x = df[df['Cost'] == minimum_y].index[0]

    # plot the data
    plt.style.use('seaborn-whitegrid')
    sns.lineplot(data=df, x=df.index, y='Cost', linewidth = 0.5)

    plt.scatter(minimum_x, minimum_y, c='green')
    plt.annotate(f'Minimum: {minimum_y}', (minimum_x - 800, minimum_y), textcoords='offset points', xytext=(-15,10), ha='center', color='green', fontsize=12)

    plt.title('Simulated Annealing')

    plt.xlabel('Iteration')
    plt.ylabel('Malus')
    
    plt.savefig('Annealing.png', dpi=1000)

    plt.show()