import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

split_indices = np.where(df['List Iterations'] == 0)[0]

dfs = np.split(df, split_indices)

list_durations = []
list_malus = []
list_multipliers = [0.1, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

for i, d in enumerate(dfs):
    if i != 0:
        list_durations.append(d['Duration since innit'].max())
        list_malus.append(d['Total Malus'].min())

df_2 = pd.DataFrame({ 
    'Multipliers': list_multipliers,
    'Durations': list_durations,
    'Malus': list_malus
})


x = np.array(list_multipliers)

figure, axis = plt.subplots()

width = 0.35
axis.bar(x - width/2, list_durations, width, label='Durations')
axis.bar(x + width/2, list_malus, width, label='Malus')

axis.set_xlabel('Multipliers')
axis.set_ylabel('Values')
axis.legend()
plt.title('Duration and Malus on different Multipliers')
plt.savefig('Duration and Malus different Multipliers.png', dpi=1000)

plt.show()