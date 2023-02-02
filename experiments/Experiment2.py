import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# export data to a csv
df = pd.read_csv(r'data/experiment2.csv')

# extract a list of used hillclimbers
hillclimbers = df['Hill Climber'].unique()

# create different dataframes for each hillclimber
df_HC1 = df[df['Hill Climber'] == hillclimbers[0]]
df_HC2 = df[df['Hill Climber'] == hillclimbers[1]]

# plot
plt.figure(figsize=(10,4))
plt.style.use('seaborn-whitegrid')
sns.lineplot(data=df_HC1, x='Iteration', y='Cost')
sns.lineplot(data=df_HC2, x='Iteration', y='Cost')
plt.savefig(r'plots/hillclimbers 3 & 4 MP.png')
