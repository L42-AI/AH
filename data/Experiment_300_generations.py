import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


if __name__ == '__main__':

    df = pd.read_csv('Hillclimber Run for 300 Generatinos Multiplier 4.csv')

    sns.lineplot(data=df, x='list_iterations', y='Iteration.1')

    minimum_y = df['Iteration.1'].min()
    minimum_x = df[df['Iteration.1'] == minimum_y].index[0]

    df['count'] = (df['Iteration.1'] != df['Iteration.1'].shift()).cumsum()
    grouped = df.groupby('count')['Iteration.1']
    longest_seq = grouped.count().idxmax()
    value = grouped.apply(lambda x: x.iloc[0]).loc[longest_seq]
    count = grouped.count().loc[longest_seq]

    plt.text(50, 1250 ,f'The score: {value} did not change for {count} generations!', color='black', )

    plt.scatter(minimum_x, minimum_y, c='green')
    plt.annotate(f'Minimum: {minimum_y}', (minimum_x, minimum_y), textcoords='offset points', xytext=(-15,10), ha='center', color='green', fontsize=12)

    plt.xlabel('Iteration')
    plt.ylabel('Malus')
    plt.title('Experiment Run Hillclimber for 300 iterations', fontsize=20)

    plt.savefig('Plot Testing Hillclimber 300 generations.png', dpi=1000)

    plt.show()