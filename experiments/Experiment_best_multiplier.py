import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv(r'data/Different Multipliers.csv')

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
plt.title('Duration and Malus of different Multipliers')
plt.savefig(r'plots/Plot Duration and Malus different Multipliers.png', dpi=1000)

plt.show()