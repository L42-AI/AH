import tkinter as tk
import matplotlib

matplotlib.use("TkAgg")

import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

import classes.GUI.selector_GUI as SelectorApp

class App(customtkinter.CTk):
    def __init__(self, process):
        super().__init__()

        self.process = process

        # configure window
        self.title("Scheduly")
        self.geometry(f"{1000}x{580}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame.grid_columnconfigure((0,1), weight=1)
        self.frame.grid_rowconfigure((0,1,2), weight=1)

        self.HC1_itr = [0,4,5,9,10,13,14,15,19,20]
        self.HC1_val = [400, 385, 376, 366, 350, 342, 341, 329, 321, 300]
        self.HC2_itr = [0,4,6,8,10,12,14,16,17,20]
        self.HC2_val = [400, 395, 386, 368, 350, 341, 331, 328, 324, 300]
        self.HC3_itr = [0,2,5,7,10,13,14,16,19,20]
        self.HC3_val = [400, 375, 374, 361, 350, 349, 346, 332, 329, 300]
        self.HC4_itr = [0,1,2,9,10,11,13,14,18,20]
        self.HC4_val = [400, 365, 376, 366, 350, 342, 341, 329, 321, 300]


        self.figure = Figure(figsize=(6,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.chart_type = FigureCanvasTkAgg(self.figure, self.frame)
        self.chart_type.get_tk_widget().grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="nsew")

        self.malus_label = customtkinter.CTkLabel(self.frame, text='Malus', font=customtkinter.CTkFont(size=30, weight="bold"))
        self.malus_label.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.malus_var = customtkinter.IntVar(self.frame)

        self.malus_count_label = customtkinter.CTkLabel(self.frame, textvariable=self.malus_var, font=customtkinter.CTkFont(size=35, weight="bold"))
        self.malus_count_label.grid(row=1, column=1, padx=20, pady=20, sticky="new")

        self.accept_button = customtkinter.CTkButton(self.frame, height=50, text="Finish", state='disabled', fg_color='red', hover_color='red', font=customtkinter.CTkFont(size=15, weight="bold"), command=self.finish)
        self.accept_button.grid(row=2, column=1, padx=40, pady=20, sticky="sew")

        self.colours = ['r', 'b', 'g', 'm']
        self.i = 0
        self.ani = animation.FuncAnimation(self.figure, self.animate, frames=10 + 1, repeat=False)
        self.chart_type.draw()


    def animate(self, i):
        self.ax.clear()
        self.ax.plot(self.HC1_itr[:self.i], self.HC1_val[:self.i], c=self.colours[0], label='HillClimber 1')
        self.ax.plot(self.HC2_itr[:self.i], self.HC2_val[:self.i], c=self.colours[1], label='HillClimber 2')
        self.ax.plot(self.HC3_itr[:self.i], self.HC3_val[:self.i], c=self.colours[2], label='HillClimber 3')
        self.ax.plot(self.HC4_itr[:self.i], self.HC4_val[:self.i], c=self.colours[3], label='HillClimber 4')
        self.ax.set_xlabel('Iterations')
        self.ax.set_ylabel('Values')
        self.ax.set_title('Dynamic Plot')
        self.ax.legend()
        self.i += 1
        self.chart_type.draw()

        lowest = min(self.HC1_val[:self.i][-1], self.HC2_val[:self.i][-1], self.HC3_val[:self.i][-1], self.HC4_val[:self.i][-1])
        self.malus_var.set(lowest)

        if lowest < 350:
            self.accept_button.configure(state='normal', fg_color='green', hover_color='green')

    def run(self):
        self.mainloop()

    def finish(self):

        self.destroy

        # finish = True

        # # Wait for the child process to finish
        # while finish:
        #     # Send the flag to the child process
        #     self.process.stdin.write(str(finish).encode())
        #     self.process.stdin.flush()

        #     # Read the output from the child process
        #     output = self.process.stdout.readline().decode()
        #     if output == 'False\n':
        #         finish = False

        self.__setup_selector_app()


    def __setup_selector_app(self) -> None:
        S_App = SelectorApp.App()
        S_App.run()

