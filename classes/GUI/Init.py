import tkinter
import tkinter.messagebox
import customtkinter

import classes.Algorithms.generator as GeneratorClass

from data.data import COURSES, STUDENT_COURSES, ROOMS


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Scheduly")
        self.geometry(f"{240}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        """ Optimize Configure Frame """

        self.toggle_frame = customtkinter.CTkFrame(self)
        self.toggle_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        self.toggle_frame.grid_columnconfigure(0, weight=1)
        self.toggle_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        self.label_algorithms_group = customtkinter.CTkLabel(master=self.toggle_frame, text="Algorithms", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_algorithms_group.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.greedy_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Greedy', font=customtkinter.CTkFont(size=13))
        self.greedy_switch.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.hillclimber_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Hill Climber', font=customtkinter.CTkFont(size=13))
        self.hillclimber_switch.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.sim_annealing_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Sim. Annealing', font=customtkinter.CTkFont(size=13))
        self.sim_annealing_switch.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.label_methods_group = customtkinter.CTkLabel(master=self.toggle_frame, text="Methods", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_methods_group.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.classes_swap_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Classes Swap', font=customtkinter.CTkFont(size=13))
        self.classes_swap_switch.grid(row=5, column=0, pady=10, padx=20, sticky="n")
        self.student_swap_switch = customtkinter.CTkSwitch(master=self.toggle_frame, text='Student Swap', font=customtkinter.CTkFont(size=13))
        self.student_swap_switch.grid(row=6, column=0, pady=10, padx=20, sticky="n")

        """ Setup Multiprocessing Button """

        # Parallel option
        self.multiprocessing_frame = customtkinter.CTkFrame(self)
        self.multiprocessing_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.multiprocessing_frame.grid_columnconfigure(0, weight=1)
        self.multiprocessing_frame.grid_rowconfigure(0, weight=1)

        self.multiprocessing_checkbox = customtkinter.CTkCheckBox(master=self.multiprocessing_frame, text='Multiprocessing', font=customtkinter.CTkFont(size=15, weight='bold'))
        self.multiprocessing_checkbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        """ Setup Generate Button """

        # Generate Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate)
        self.generate_button.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        # Generate Optimal Button
        self.generate_optimal_button = customtkinter.CTkButton(master=self, text="Generate Optimal", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate_optimal)
        self.generate_optimal_button.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")

    def generate(self):
        greedy = self.greedy_switch.get()
        hill_climbing = self.hillclimber_switch.get()
        sim_annealing = self.sim_annealing_switch.get()

        classes_swap = self.classes_swap_switch.get()
        student_swap = self.student_swap_switch.get()

        multiprocessing = self.multiprocessing_checkbox.get()

        arguments = [COURSES, STUDENT_COURSES, ROOMS]



        if greedy:
            arguments.append(capacity=True, popular=True, popular_own_day=True)

        if hill_climbing:
            arguments.append(climbing=True)

        if sim_annealing:
            arguments.append(annealing=True)

        if classes_swap:
            arguments.append(classes_swap=True)

        if student_swap:
            arguments.append(student_swap=True)

        if multiprocessing:
            arguments.append(multiprocessing=True)

        arguments = tuple(arguments)

        print(arguments)

        if not hill_climbing:
            G = GeneratorClass.Generator(arguments)

        elif not sim_annealing:
            G = GeneratorClass.Generator_HC(arguments)

        else:
            G = GeneratorClass.Generator_SA(arguments)


        pass
    def generate_optimal(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()