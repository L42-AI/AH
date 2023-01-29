import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('generator_data.csv')
HC1_x_values = data['HC1 iterations']
HC1_y_values = data['HC1 values']
HC2_x_values = data['HC2 iterations']
HC2_y_values = data['HC2 values']
HC3_x_values = data['HC3 iterations']
HC3_y_values = data['HC3 values']
HC4_x_values = data['HC4 iterations']
HC4_y_values = data['HC4 values']

fig = plt.figure(figsize=(15, 7))

ax1 = plt.subplot2grid((4,8), (0,0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid((4,8), (0,2), colspan=2, rowspan=2)
ax3 = plt.subplot2grid((4,8), (2,0), colspan=2, rowspan=2)
ax4 = plt.subplot2grid((4,8), (2,2), colspan=2, rowspan=2)
ax5 = plt.subplot2grid((4,8), (0,4), colspan=4, rowspan=4)

ax1.plot(HC1_x_values, HC1_y_values, c='r', label='HC1')
ax2.plot(HC2_x_values, HC2_y_values, c='g', label='HC2')
ax3.plot(HC3_x_values, HC3_y_values, c='b', label='HC3')
ax4.plot(HC4_x_values, HC4_y_values, c='m', label='HC4')
ax5.plot(HC1_x_values, HC1_y_values, c='r', label='HC1')
ax5.plot(HC2_x_values, HC2_y_values, c='g', label='HC2')
ax5.plot(HC3_x_values, HC3_y_values, c='b', label='HC3')
ax5.plot(HC4_x_values, HC4_y_values, c='m', label='HC4')

ax5.legend(loc='upper right')
plt.tight_layout()
plt.show()