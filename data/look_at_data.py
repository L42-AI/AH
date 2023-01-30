import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# df = pd.read_csv('Normal Hillclimber geen multiplier 30 keer.csv')

# threshold = 400
# max_iteration = 330

# df_2 = df[df['Total Malus'] <= threshold]
# df_2 = df_2[df_2['Iteration'] <= max_iteration]

# sns.lineplot(data=df, x='Unnamed: 0', y='Total Malus')
# plt.xlabel('Iterations')
# plt.title('Run the Hillclimber 30 times')
# sns.lineplot(data=df_2, x='Iteration', y='Total Malus')
# plt.title('Average of the 30 Hillclimbers')

# plt.show()

# plt.savefig('Plot show all 30 climbers.png', dpi=1000)

# print(df)

df = pd.read_csv('Different Multipliers.csv')

sns.lineplot(data=df, x='Unnamed: 0', y='Total Malus')

plt.show()
# print(df)