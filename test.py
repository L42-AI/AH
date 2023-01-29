import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure

def animate(i):
    data = pd.read_csv('generator_data.csv')
    HC1_x_values = data['HC1 iterations']
    HC1_y_values = data['HC1 values']
    HC2_x_values = data['HC2 iterations']
    HC2_y_values = data['HC2 values']
    HC3_x_values = data['HC3 iterations']
    HC3_y_values = data['HC3 values']
    HC4_x_values = data['HC4 iterations']
    HC4_y_values = data['HC4 values']

    plt.clf()
    fig, ax = plt.subplots(2, 2)

    ax[0][0].plot(HC1_x_values, HC1_y_values, c='r', label='HC1')
    ax[0][1].plot(HC2_x_values, HC2_y_values, c='g', label='HC2')
    ax[1][0].plot(HC3_x_values, HC3_y_values, c='b', label='HC3')
    ax[1][1].plot(HC4_x_values, HC4_y_values, c='m', label='HC4')

    plt.legend(loc='upper right')
    plt.tight_layout()

    fig2 = plt.figure()
    plt.plot(HC1_x_values, HC1_y_values, c='r', label='HC1')
    plt.plot(HC2_x_values, HC2_y_values, c='g', label='HC2')
    plt.plot(HC3_x_values, HC3_y_values, c='b', label='HC3')
    plt.plot(HC4_x_values, HC4_y_values, c='m', label='HC4')
    plt.legend(loc='upper right')
    plt.tight_layout()

    ax.close()
    fig2.close()

figure = Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)

ani = FuncAnimation(figure, animate, frames=10 + 1, repeat=False)

plt.tight_layout()
plt.show()
