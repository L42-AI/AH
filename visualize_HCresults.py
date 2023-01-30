import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/HCresults.csv')

# print(df.columns)

HC1_label = df['HC1 type']
HC1_label.dropna(inplace=True)

HC1_x_values = df['HC1 iteration']
HC1_x_values.dropna(inplace=True)

HC1_y_values = df['HC1 malus']
HC1_y_values.dropna(inplace=True)

HC2_label = df['HC2 type']
HC2_label.dropna(inplace=True)
HC2_x_values = df['HC2 iteration']
HC2_x_values.dropna(inplace=True)
HC2_y_values = df['HC2 malus']
HC2_y_values.dropna(inplace=True)

HC3_label = df['HC3 type']
HC3_label.dropna(inplace=True)
HC3_x_values = df['HC3 iteration']
HC3_x_values.dropna(inplace=True)
HC3_y_values = df['HC3 malus']
HC3_y_values.dropna(inplace=True)

HC4_label = df['HC4 type']
HC4_label.dropna(inplace=True)
HC4_x_values = df['HC4 iteration']
HC4_x_values.dropna(inplace=True)
HC4_y_values = df['HC4 malus']
HC4_y_values.dropna(inplace=True)


print(HC1_label.unique())
print(HC2_label.unique())
print(HC3_label.unique())
print(HC4_label.unique())

fig = plt.figure(figsize=(14, 7))

ax1 = plt.subplot2grid((4,8), (0,0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid((4,8), (0,2), colspan=2, rowspan=2)
ax3 = plt.subplot2grid((4,8), (2,0), colspan=2, rowspan=2)
ax4 = plt.subplot2grid((4,8), (2,2), colspan=2, rowspan=2)
ax5 = plt.subplot2grid((4,8), (0,4), colspan=4, rowspan=4)

ax1.plot(HC1_x_values.to_list(), HC1_y_values.to_list(), c='r', label=HC1_label.unique()[0])
ax2.plot(HC2_x_values.to_list(), HC2_y_values.to_list(), c='g', label=HC2_label.unique()[0])
ax3.plot(HC3_x_values.to_list(), HC3_y_values.to_list(), c='b', label=HC3_label.unique()[0])
ax4.plot(HC4_x_values.to_list(), HC4_y_values.to_list(), c='m', label=HC4_label.unique()[0])

ax5.plot(HC1_x_values.to_list(), HC1_y_values.to_list(), c='r', label=HC1_label.unique()[0])
ax5.plot(HC2_x_values.to_list(), HC2_y_values.to_list(), c='g', label=HC2_label.unique()[0])
ax5.plot(HC3_x_values.to_list(), HC3_y_values.to_list(), c='b', label=HC3_label.unique()[0])
ax5.plot(HC4_x_values.to_list(), HC4_y_values.to_list(), c='m', label=HC4_label.unique()[0])

ax1.legend(loc='upper right')
ax2.legend(loc='upper right')
ax3.legend(loc='upper right')
ax4.legend(loc='upper right')
ax5.legend(loc='upper right')
plt.tight_layout()
plt.show()