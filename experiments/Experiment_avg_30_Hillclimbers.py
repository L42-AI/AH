import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':

    # load the data into a dataframe
    df = pd.read_csv(r'data/Normal Hillclimber geen multiplier 30 keer.csv')

    # set the phrame for the graph
    threshold = 400
    max_iteration = 330

    # get only the data inside of the phrame size we want
    df_2 = df[df['Total Malus'] <= threshold]
    df_2 = df_2[df_2['Iteration'] <= max_iteration]

    # plot and save the graph
    sns.lineplot(data=df_2, x='Iteration', y='Total Malus')
    plt.title('Average of the 30 Hillclimbers')

    plt.savefig(r'plots/Plot Average of the 30 Hillclimbers.png')

    plt.show()
