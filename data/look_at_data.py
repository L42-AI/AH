import pandas as pd

runs_30 = pd.read_csv('Normal Hillclimber geen multiplier 30 keer.csv')

print(runs_30['Total Malus'].min())