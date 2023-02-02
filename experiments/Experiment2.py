import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


df = pd.read_csv('experiments/experiment2.csv')

hillclimbers = df['Hill Climber'].unique()

df_HC1 = df[df['Hill Climber'] == hillclimbers[0]]
df_HC2 = df[df['Hill Climber'] == hillclimbers[1]]

plt.figure(figsize=(10,4))
plt.style.use('seaborn-whitegrid')
sns.lineplot(data=df_HC1, x='Iteration', y='Cost')
sns.lineplot(data=df_HC2, x='Iteration', y='Cost')
plt.show()
