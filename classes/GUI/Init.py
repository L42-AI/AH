import tkinter
import tkinter.messagebox
import customtkinter

import classes.algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Scheduly")
        self.geometry(f"{250}x{300}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        """ Optimize Configure Frame """

        self.toggle_frame = customtkinter.CTkFrame(self)
        self.toggle_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        self.toggle_frame.grid_columnconfigure(0, weight=1)
        self.toggle_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        self.label_initialization = customtkinter.CTkLabel(master=self.toggle_frame, text="Initialize", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_initialization.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.greedy_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Greedy', font=customtkinter.CTkFont(size=15))
        self.greedy_switch.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        # self.hillclimber_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Hill Climber', font=customtkinter.CTkFont(size=13))
        # self.hillclimber_switch.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        # self.sim_annealing_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Sim. Annealing', font=customtkinter.CTkFont(size=13))
        # self.sim_annealing_switch.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.label_optimization = customtkinter.CTkLabel(master=self.toggle_frame, text="Optimize", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_optimization.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.annealing_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Simulates annealing', font=customtkinter.CTkFont(size=15))
        self.annealing_switch.grid(row=5, column=0, pady=10, padx=20, sticky="nsew")
        # self.student_swap_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Student Swap', font=customtkinter.CTkFont(size=13))
        # self.student_swap_switch.grid(row=6, column=0, pady=10, padx=20, sticky="n")

        """ Setup Multiprocessing Button """

        # # Parallel option
        # self.multiprocessing_frame = customtkinter.CTkFrame(self)
        # self.multiprocessing_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        # self.multiprocessing_frame.grid_columnconfigure(0, weight=1)
        # self.multiprocessing_frame.grid_rowconfigure(0, weight=1)

        # self.multiprocessing_checkbox = customtkinter.CTkCheckBox(master=self.multiprocessing_frame, text='Multiprocessing', font=customtkinter.CTkFont(size=15, weight='bold'))
        # self.multiprocessing_checkbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        """ Setup Generate Button """

        # Generate Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate)
        self.generate_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # # Generate Optimal Button
        # self.generate_optimal_button = customtkinter.CTkButton(master=self, text="Generate Optimal", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate_optimal)
        # self.generate_optimal_button.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

    def run(self):
        self.mainloop()

    def generate(self):

        # Set all arguments to False
        capacity = False
        popular = False
        popular_own_day = False

        # Collect state of all widgets
        greedy = self.greedy_switch.get()
        annealing = self.annealing_switch.get()

        # Set arguments true based on input of widget state
        if greedy:
            capacity = True
            popular = True
            popular_own_day = True
        run = self.generate_button
        if run:
            self.destroy()
            G = GeneratorClass.Generator(COURSES, STUDENT_COURSES, ROOMS,\
            capacity, popular, popular_own_day, annealing=annealing)

        # Run optimizing
        G.optimize()