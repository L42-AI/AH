import customtkinter

import classes.algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS

import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

import subprocess

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()


        self.ax = plt.figure(figsize=(14, 7))

        # configure window
        self.title("Scheduly")
        self.geometry(f"{250}x{350}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        """ Optimize Configure Frame """

        self.toggle_frame = customtkinter.CTkFrame(self)
        self.toggle_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        self.toggle_frame.grid_columnconfigure(0, weight=1)
        self.toggle_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)

        self.label_initialization = customtkinter.CTkLabel(master=self.toggle_frame, text="Initialize", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_initialization.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.greedy_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Greedy', font=customtkinter.CTkFont(size=15), command=self.greedy_switch_click)
        self.greedy_switch.grid(row=1, column=0, pady=10, padx=20, sticky="n")

        self.label_optimization = customtkinter.CTkLabel(master=self.toggle_frame, text="Optimize", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_optimization.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")

        self.hill_climbing_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Hill Climbing', font=customtkinter.CTkFont(size=15), command=self.hillclimber_switch_click)
        self.hill_climbing_switch.grid(row=7, column=0, pady=10, padx=20, sticky="nsew")

        """ Setup Generate Button """

        # Generate Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate)
        self.generate_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    def run(self) -> None:
        self.mainloop()

    def hillclimber_switch_click(self) -> None:

        state_hc = self.hill_climbing_switch.get()

        if state_hc == 1:
            self.annealing_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Sim. Annealing', font=customtkinter.CTkFont(size=15))
            self.annealing_switch.grid(row=8, column=0, padx=20, pady=10, sticky="nsew")
        else:
            self.annealing_switch.destroy()

    def greedy_switch_click(self) -> None:

        state_greedy = self.greedy_switch.get()

        if state_greedy == 1:
            self.capacity_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Capacity', font=customtkinter.CTkFont(size=15))
            self.capacity_switch.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

            self.popular_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Popular first', font=customtkinter.CTkFont(size=15), command=self.turn_off_difficult_P)
            self.popular_switch.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

            self.popular_own_day_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Largest first', font=customtkinter.CTkFont(size=15), command=self.turn_off_difficult_POD)
            self.popular_own_day_switch.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

            self.difficult_students_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Busy Students', font=customtkinter.CTkFont(size=15), command=self.turn_off_popular)
            self.difficult_students_switch.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

            self.geometry(f"{250}x{525}")
        else:
            self.capacity_switch.destroy()
            self.popular_switch.destroy()
            self.popular_own_day_switch.destroy()
            self.difficult_students_switch.destroy()

            self.geometry(f"{250}x{350}")

    def turn_off_difficult_POD(self) -> None:
        state_popular_own_day = self.popular_own_day_switch.get()
        if state_popular_own_day == 1:
            self.difficult_students_switch.deselect()

    def turn_off_difficult_P(self) -> None:
        state_popular = self.popular_switch.get()
        if state_popular == 1:
            self.difficult_students_switch.deselect()

    def turn_off_popular(self) -> None:
        state_difficult = self.difficult_students_switch.get()
        if state_difficult == 1:
            self.popular_own_day_switch.deselect()
            self.popular_switch.deselect()

    def generate(self) -> None:

        # Extract state_data from GUI
        settings = self.__set_data()

        # Destroy window
        self.destroy()

        self.export_data(settings)

        self.__run_algorithm()

        # self.plot_progress()

    def __set_data(self) -> tuple:

        # Collect state of hill climbing switch
        hill_climbing = self.hill_climbing_switch.get()

        # Set setting for initialization plot or optimalization
        if hill_climbing:
            visualize = False
        else:
            visualize = True

        # Try all other switches on state
        try:
            capacity = bool(self.capacity_switch.get())
        except:
            capacity = False

        try:
            popular = bool(self.popular_switch.get())
        except:
            popular = False

        try:
            popular_own_day = bool(self.popular_own_day_switch.get())
        except:
            popular_own_day = False

        try:
            difficult_students = bool(self.difficult_students_switch.get())
        except:
            difficult_students = False

        try:
            annealing = bool(self.annealing_switch.get())
        except:
            annealing = False

        return capacity, popular, popular_own_day, difficult_students, annealing, visualize

    def export_data(self, settings) -> None:

        capacity, popular, popular_own_day, difficult_students, annealing, visualize = settings

        dictionary = {
            'capacity': capacity,
            'popular': popular,
            'popular_own_day': popular_own_day,
            'difficult_students': difficult_students,
            'annealing': annealing,
            'visualize': visualize,
        }
        with open('data/settings.json', 'w') as f:
            json.dump(dictionary, f)

    def __run_algorithm(self) -> None:

        with open('data/terminate.txt', 'w') as f:
                f.write('False')

        subprocess.Popen(['python3', 'run_algorithm.py'])

    def plot_progress(self) -> None:

        while True:
            with open('data/terminate.txt', 'r') as f:
                finished = f.read()
                if finished == 'True':
                    plt.close()
                    break

            df = pd.read_csv('data/HCresults.csv')

            HC1_x_values = df['HC1 iteration']
            HC1_x_values.dropna(inplace=True)

            HC1_y_values = df['HC1 malus']
            HC1_y_values.dropna(inplace=True)

            HC2_x_values = df['HC2 iteration']
            HC2_x_values.dropna(inplace=True)

            HC2_y_values = df['HC2 malus']
            HC2_y_values.dropna(inplace=True)

            HC3_x_values = df['HC3 iteration']
            HC3_x_values.dropna(inplace=True)

            HC3_y_values = df['HC3 malus']
            HC3_y_values.dropna(inplace=True)

            HC4_x_values = df['HC4 iteration']
            HC4_x_values.dropna(inplace=True)

            HC4_y_values = df['HC4 malus']
            HC4_y_values.dropna(inplace=True)

            plt.plot(HC1_x_values.to_list(), HC1_y_values.to_list(), c='r', label='HC1')
            plt.plot(HC2_x_values.to_list(), HC2_y_values.to_list(), c='g', label='HC2')
            plt.plot(HC3_x_values.to_list(), HC3_y_values.to_list(), c='b', label='HC3')
            plt.plot(HC4_x_values.to_list(), HC4_y_values.to_list(), c='m', label='HC4')

            plt.pause(0.0001)


