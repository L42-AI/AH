import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import time
# data = pd.read_csv('generator_data.csv')
# HC1_x_values = data['HC1 iterations']
# HC1_y_values = data['HC1 values']
# HC2_x_values = data['HC2 iterations']
# HC2_y_values = data['HC2 values']
# HC3_x_values = data['HC3 iterations']
# HC3_y_values = data['HC3 values']
# HC4_x_values = data['HC4 iterations']
# HC4_y_values = data['HC4 values']

# fig = plt.figure(figsize=(14, 7))

# ax1 = plt.subplot2grid((4,8), (0,0), colspan=2, rowspan=2)
# ax2 = plt.subplot2grid((4,8), (0,2), colspan=2, rowspan=2)
# ax3 = plt.subplot2grid((4,8), (2,0), colspan=2, rowspan=2)
# ax4 = plt.subplot2grid((4,8), (2,2), colspan=2, rowspan=2)
# ax5 = plt.subplot2grid((4,8), (0,4), colspan=4, rowspan=4)

# ax1.plot(HC1_x_values, HC1_y_values, c='r', label='HC1')
# ax2.plot(HC2_x_values, HC2_y_values, c='g', label='HC2')
# ax3.plot(HC3_x_values, HC3_y_values, c='b', label='HC3')
# ax4.plot(HC4_x_values, HC4_y_values, c='m', label='HC4')
# ax5.plot(HC1_x_values, HC1_y_values, c='r', label='HC1')
# ax5.plot(HC2_x_values, HC2_y_values, c='g', label='HC2')
# ax5.plot(HC3_x_values, HC3_y_values, c='b', label='HC3')
# ax5.plot(HC4_x_values, HC4_y_values, c='m', label='HC4')

# ax5.legend(loc='upper right')
# plt.tight_layout()
# plt.show()

# import matplotlib.pyplot as plt
# import pandas as pd
# from matplotlib.animation import FuncAnimation

# data = pd.read_csv('generator_data.csv')
# HC1_x_values = data['HC1 iterations']
# HC1_y_values = data['HC1 values']
# HC2_x_values = data['HC2 iterations']
# HC2_y_values = data['HC2 values']
# HC3_x_values = data['HC3 iterations']
# HC3_y_values = data['HC3 values']
# HC4_x_values = data['HC4 iterations']
# HC4_y_values = data['HC4 values']

# fig, ax = plt.subplots(figsize=(14, 7))
# ax.set_xlim(0, max(HC1_x_values))
# ax.set_ylim(min(min(HC1_y_values), min(HC2_y_values), min(HC3_y_values), min(HC4_y_values)),
# max(max(HC1_y_values), max(HC2_y_values), max(HC3_y_values), max(HC4_y_values)))

# line1, = ax.plot([], [], c='r', label='HC1')
# line2, = ax.plot([], [], c='g', label='HC2')
# line3, = ax.plot([], [], c='b', label='HC3')
# line4, = ax.plot([], [], c='m', label='HC4')
# ax.legend(loc='upper right')

# def init():
# line1.set_data([], [])
# line2.set_data([], [])
# line3.set_data([], [])
# line4.set_data([], [])
# return line1, line2, line3, line4

# def animate(i):
# line1.set_data(HC1_x_values[:i], HC1_y_values[:i])
# line2.set_data(HC2_x_values[:i], HC2_y_values[:i])
# line3.set_data(HC3_x_values[:i], HC3_y_values[:i])
# line4.set_data(HC4_x_values[:i], HC4_y_values[:i])
# return line1, line2, line3, line4

# ani = FuncAnimation(fig, animate, frames=len(HC1_x_values), init_func=init, blit=True)
# plt.tight_layout()
# plt.show()

# import matplotlib.pyplot as plt
# import pandas as pd
# from matplotlib.animation import FuncAnimation

# data = pd.read_csv('generator_data.csv')
# HC1_x_values = data['HC1 iterations']
# HC1_y_values = data['HC1 values']
# HC2_x_values = data['HC2 iterations']
# HC2_y_values = data['HC2 values']
# HC3_x_values = data['HC3 iterations']
# HC3_y_values = data['HC3 values']
# HC4_x_values = data['HC4 iterations']
# HC4_y_values = data['HC4 values']

# fig = plt.figure(figsize=(14, 7))

# ax1 = plt.subplot2grid((4,8), (0,0), colspan=2, rowspan=2)
# ax2 = plt.subplot2grid((4,8), (0,2), colspan=2, rowspan=2)
# ax3 = plt.subplot2grid((4,8), (2,0), colspan=2, rowspan=2)
# ax4 = plt.subplot2grid((4,8), (2,2), colspan=2, rowspan=2)
# ax5 = plt.subplot2grid((4,8), (0,4), colspan=4, rowspan=4)

# line1, = ax1.plot([], [], c='r', label='HC1')
# line2, = ax2.plot([], [], c='g', label='HC2')
# line3, = ax3.plot([], [], c='b', label='HC3')
# line4, = ax4.plot([], [], c='m', label='HC4')
# line5, = ax5.plot([], [], c='r', label='HC1')
# line6, = ax5.plot([], [], c='g', label='HC2')
# line7, = ax5.plot([], [], c='b', label='HC3')
# line8, = ax5.plot([], [], c='m', label='HC4')

# ax5.legend(loc='upper right')
# plt.tight_layout()

# def update(frame):
#     data = pd.read_csv('generator_data.csv')
#     HC1_x_values = data['HC1 iterations']
#     HC1_y_values = data['HC1 values']
#     HC2_x_values = data['HC2 iterations']
#     HC2_y_values = data['HC2 values']
#     HC3_x_values = data['HC3 iterations']
#     HC3_y_values = data['HC3 values']
#     HC4_x_values = data['HC4 iterations']
#     HC4_y_values = data['HC4 values']

#     line1.set_data(HC1_x_values, HC1_y_values)
#     line2.set_data(HC2_x_values, HC2_y_values)
#     line3.set_data(HC3_x_values, HC3_y_values)
#     line4.set_data(HC4_x_values, HC4_y_values)
#     line5.set_data(HC1_x_values, HC1_y_values)
#     line6.set_data(HC2_x_values, HC2_y_values)
#     line7.set_data(HC3_x_values, HC3_y_values)
#     line8.set_data(HC4_x_values, HC4_y_values)

# '''------------------------'''

# import matplotlib.pyplot as plt
# import pandas as pd
# import matplotlib.animation as animation

# fig, ax = plt.subplots(2,2, figsize=(14,7))

# HC1_x_values = []
# HC1_y_values = []
# HC2_x_values = []
# HC2_y_values = []
# HC3_x_values = []
# HC3_y_values = []
# HC4_x_values = []
# HC4_y_values = []

# def update_data():
#     global HC1_x_values, HC1_y_values, HC2_x_values, HC2_y_values, HC3_x_values, HC3_y_values, HC4_x_values, HC4_y_values

#     data = pd.read_csv('generator_data.csv')
#     if data['HC1 type'].values[-1] != None:
#         HC1_x_values.append(data['HC1 iterations'].values[-1])
#         HC1_y_values.append(data['HC1 values'].values[-1])
#     elif data['HC2 type'].values[-1] != None:
#         HC2_x_values.append(data['HC2 iterations'].values[-1])
#         HC2_y_values.append(data['HC2 values'].values[-1])
#     elif data['HC3 type'].values[-1] != None:
#         HC3_x_values.append(data['HC3 iterations'].values[-1])
#         HC3_y_values.append(data['HC3 values'].values[-1])
#     elif data['HC4 type'].values[-1] != None:
#         HC4_x_values.append(data['HC4 iterations'].values[-1])
#         HC4_y_values.append(data['HC4 values'].values[-1])

# def animate(i):
#     update_data()

#     ax[0][0].clear()
#     ax[0][0].plot(HC1_x_values, HC1_y_values, c='r', label='HC1')

#     ax[0][1].clear()
#     ax[0][1].plot(HC2_x_values, HC2_y_values, c='g', label='HC2')

#     ax[1][0].clear()
#     ax[1][0].plot(HC3_x_values, HC3_y_values, c='b', label='HC3')

#     ax[1][1].clear()
#     ax[1][1].plot(HC4_x_values, HC4_y_values, c='m', label='HC4')

# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.tight_layout()
# plt.show()

# fig = plt.figure(figsize=(14, 7))

# ax1 = plt.subplot2grid((4,8), (0,0), colspan=2, rowspan=2)
# ax2 = plt.subplot2grid((4,8), (0,2), colspan=2, rowspan=2)
# ax3 = plt.subplot2grid((4,8), (2,0), colspan=2, rowspan=2)
# ax4 = plt.subplot2grid((4,8), (2,2), colspan=2, rowspan=2)
# ax5 = plt.subplot2grid((4,8), (0,4), colspan=4, rowspan=4)

# ax5.legend(loc='upper right')

# while True:
#     with open('data/terminate.txt', 'r') as f:
#         finished = f.read()
#         if finished:
#             break

#     df = pd.read_csv('data/HCresults.csv')

#     HC1_x_values = df['HC1 iteration']
#     HC1_x_values.dropna(inplace=True)

#     HC1_y_values = df['HC1 malus']
#     HC1_y_values.dropna(inplace=True)

#     HC2_x_values = df['HC2 iteration']
#     HC2_x_values.dropna(inplace=True)

#     HC2_y_values = df['HC2 malus']
#     HC2_y_values.dropna(inplace=True)

#     HC3_x_values = df['HC3 iteration']
#     HC3_x_values.dropna(inplace=True)

#     HC3_y_values = df['HC3 malus']
#     HC3_y_values.dropna(inplace=True)

#     HC4_x_values = df['HC4 iteration']
#     HC4_x_values.dropna(inplace=True)

#     HC4_y_values = df['HC4 malus']
#     HC4_y_values.dropna(inplace=True)

#     ax1.plot(HC1_x_values, HC1_y_values, c='r', label='HC1')
#     ax2.plot(HC2_x_values, HC2_y_values, c='g', label='HC2')
#     ax3.plot(HC3_x_values, HC3_y_values, c='b', label='HC3')
#     ax4.plot(HC4_x_values, HC4_y_values, c='m', label='HC4')

#     ax5.plot(HC1_x_values, HC1_y_values, c='r', label='HC1')
#     ax5.plot(HC2_x_values, HC2_y_values, c='g', label='HC2')
#     ax5.plot(HC3_x_values, HC3_y_values, c='b', label='HC3')
#     ax5.plot(HC4_x_values, HC4_y_values, c='m', label='HC4')

#     plt.pause(0.001)

# plt.show()


print(time.time())