import tkinter
import tkinter.messagebox
import customtkinter

import os
import json

import subprocess

import classes.algorithms.generator as GeneratorClass
import classes.GUI.generator_GUI as GeneratorApp

from data.data import COURSES, STUDENT_COURSES, ROOMS


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

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
        self.toggle_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)

        self.label_initialization = customtkinter.CTkLabel(master=self.toggle_frame, text="Initialize", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_initialization.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.greedy_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Greedy', font=customtkinter.CTkFont(size=15))
        self.greedy_switch.grid(row=1, column=0, pady=10, padx=20, sticky="n")

        self.label_optimization = customtkinter.CTkLabel(master=self.toggle_frame, text="Optimize", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_optimization.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.hill_climbing_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Hill Climbing', font=customtkinter.CTkFont(size=15), command=self.hillclimber_switch_click)
        self.hill_climbing_switch.grid(row=5, column=0, pady=10, padx=20, sticky="nsew")

        """ Setup Generate Button """

        # Generate Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate)
        self.generate_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    def run(self) -> None:
        self.mainloop()

    def hillclimber_switch_click(self) -> None:

        state = self.hill_climbing_switch.get()

        if state == 1:
            self.annealing_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Sim. Annealing', font=customtkinter.CTkFont(size=15))
            self.annealing_switch.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")
        else:
            self.annealing_switch.destroy()

    def generate(self) -> None:

        # Extract state_data from GUI
        algorithm_settings = self.__set_data()

        # Destroy window
        self.destroy()

        self.__export_settings(algorithm_settings)
        print('Run')
        algorithm_process = self.__run_algorithm()
        print('Execute')
        self.__setup_generator_app(algorithm_process)



    def __set_data(self) -> dict:

        # Set all arguments to False
        visualize = False
        capacity = False
        popular = False
        popular_own_day = False

        # Collect state of all widgets
        greedy = self.greedy_switch.get()
        hill_climbing = self.hill_climbing_switch.get()

        try:
            annealing = self.annealing_switch.get()
        except:
            annealing = False

        # Set arguments true based on input of widget state
        if greedy:
            capacity = True
            popular = True
            popular_own_day = True

        settings = {"capacity": capacity, "popular": popular,
                    "popular_own_day": popular_own_day,
                    "hill_climbing": hill_climbing,
                    "annealing": annealing, "visualize": visualize}

        return settings

    def __run_algorithm(self) -> object:

        algorithm_process = subprocess.Popen(['python', 'run_algorithm.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return algorithm_process

    def __export_settings(self, algorithm_settings) -> None:
        with open('data/settings.json', 'w') as f:
            json.dump(algorithm_settings, f)

    def __setup_generator_app(self, algorithm_process) -> None:
        G_App = GeneratorApp.App(algorithm_process)
        G_App.run()
