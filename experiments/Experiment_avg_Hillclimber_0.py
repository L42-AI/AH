import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':

    """ 
    This csv file has as columns Swap Students as well, however the Swap Random Seminar Hillclimber was only used.
    This is simply a mistake of putting in the wrong headers. The data is still correct.
    """
    
    zoomed = False


    # load the data into a dataframe
    df = pd.read_csv('Testing Hillclimber_0 30 times.csv')

    if zoomed:
        # cut so the plot is prittier
        df = df[df['Iteration.1'] <= 400]
        df = df_2[df_2['list_iterations'] <= 300]
    
    # plot and save the graph
    plt.figure(figsize=(10, 4))
    plt.style.use('seaborn-whitegrid')

    sns.lineplot(data=df, x='list_iterations', y='Iteration.1')
    plt.title('Average of Swap Random Seminars')


    plt.title('Average of Swap Random Seminars')
    plt.xlabel('Iteration')
    plt.ylabel('Malus')

    plt.savefig('Plot Average Seminars Swap.png', dpi=1000)

    plt.show()
