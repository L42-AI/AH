import random
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()

figure = plt.Figure(figsize=(5, 4), dpi=100)
ax = figure.add_subplot(111)
line = FigureCanvasTkAgg(figure, root)
line.get_tk_widget().pack()

def generate_data():
    """
    This function generates data points and appends them to a list
    """
    data = []
    for i in range(100):
        data.append(random.randint(0,100))
    return data

def update_plot():
    """
    This function updates the plot with new data
    """
    data = generate_data()
    ax.clear()
    ax.plot(data)
    ax.set_title('Real-time Data')
    line.draw()
    root.after(100, update_plot)

root.after(100, update_plot)
root.mainloop()
