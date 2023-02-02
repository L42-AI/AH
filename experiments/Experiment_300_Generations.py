import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

if __name__ == '__main__':

    df = pd.read_csv(r'data/Hillclimber Run for 300 Generatinos Multiplier 4.csv')

    sns.lineplot(data=df, x=df.index, y='Iteration.1')

    # get the lowest malus and their itirations
    minimum_y = df['Iteration.1'].min()
    minimum_x = df[df['Iteration.1'] == minimum_y].index[0]

    # get the longest amount of time the maluspoints were the same and the malus
    df['count'] = (df['Iteration.1'] != df['Iteration.1'].shift()).cumsum()
    grouped = df.groupby('Iteration.1')['count']
    malus = grouped.count().idxmax()
    length_of_longest_seq = grouped.count().loc[malus]

    # plot the graph
    plt.scatter(minimum_x, minimum_y, c='green')
    plt.annotate(f'Minimum: {minimum_y}', (minimum_x, minimum_y - 20), textcoords='offset points', xytext=(-15,10), ha='center', color='green', fontsize=12)

    plt.text(20, 1250, f'At malus: {malus} the score stayed the same for {length_of_longest_seq} Generations')

    plt.xlabel('Iteration')
    plt.ylabel('Malus')

    plt.title('Run Hillclimber for 300 Generations')

    plt.savefig(r'plots/Plot Hillcimber 300 Generations.png')

    plt.show()