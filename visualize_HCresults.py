import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/HCresults.csv')

print(df.columns)

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

fig = plt.figure(figsize=(14, 7))

ax1 = plt.subplot2grid((4,8), (0,0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid((4,8), (0,2), colspan=2, rowspan=2)
ax3 = plt.subplot2grid((4,8), (2,0), colspan=2, rowspan=2)
ax4 = plt.subplot2grid((4,8), (2,2), colspan=2, rowspan=2)
ax5 = plt.subplot2grid((4,8), (0,4), colspan=4, rowspan=4)

HC1_label = ''
HC1_x_values = []
HC1_y_values = []

HC2_label = ''
HC2_x_values = []
HC2_y_values = []

HC3_label = ''
HC3_x_values = []
HC3_y_values = []

HC4_label = ''
HC4_x_values = []
HC4_y_values = []

def update_data():
    global HC1_label, HC1_x_values, HC1_y_values, HC2_label, HC2_x_values, HC2_y_values, HC3_label, HC3_x_values, HC3_y_values, HC4_label, HC4_x_values, HC4_y_values

    data = pd.read_csv('generator_data.csv')
    if data['HC1 type'].values[-1] != None:
        HC1_label = data['HC1 type'].values[-1]
        HC1_x_values.append(data['HC1 iterations'].values[-1])
        HC1_y_values.append(data['HC1 values'].values[-1])
    elif data['HC2 type'].values[-1] != None:
        HC2_label = data['HC2 type'].values[-1]
        HC2_x_values.append(data['HC2 iterations'].values[-1])
        HC2_y_values.append(data['HC2 values'].values[-1])
    elif data['HC3 type'].values[-1] != None:
        HC3_label = data['HC3 type'].values[-1]
        HC3_x_values.append(data['HC3 iterations'].values[-1])
        HC3_y_values.append(data['HC3 values'].values[-1])
    elif data['HC4 type'].values[-1] != None:
        HC4_label = data['HC4 type'].values[-1]
        HC4_x_values.append(data['HC4 iterations'].values[-1])
        HC4_y_values.append(data['HC4 values'].values[-1])

for _ in range (1000):
    update_data()
    ax1.plot(HC1_x_values, HC1_y_values, c='r', label=HC1_label)
    ax2.plot(HC2_x_values, HC2_y_values, c='g', label=HC2_label)
    ax3.plot(HC3_x_values, HC3_y_values, c='b', label=HC3_label)
    ax4.plot(HC4_x_values, HC4_y_values, c='m', label=HC4_label)

    ax5.plot(HC1_x_values, HC1_y_values, c='r', label=HC1_label)
    ax5.plot(HC2_x_values, HC2_y_values, c='g', label=HC2_label)
    ax5.plot(HC3_x_values, HC3_y_values, c='b', label=HC3_label)
    ax5.plot(HC4_x_values, HC4_y_values, c='m', label=HC4_label)

    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')
    ax3.legend(loc='upper right')
    ax4.legend(loc='upper right')
    ax5.legend(loc='upper right')

    plt.tight_layout()
    plt.show()