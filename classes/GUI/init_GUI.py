import customtkinter
import csv
import classes.algorithms.generator as GeneratorClass
import classes.GUI.selector_GUI as SelectorApp
import pickle

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
       
        # configure window
        self.title("Scheduly")
        self.geometry(f"{250}x{400}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        """ Optimize Configure Frame """
        
        self.toggle_frame = customtkinter.CTkFrame(self)
        self.toggle_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        self.toggle_frame.grid_columnconfigure(0, weight=1)
        self.toggle_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        self.label_experiment = customtkinter.CTkLabel(master=self.toggle_frame, text="Experiments:", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_experiment.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.experiment1_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 1', font=customtkinter.CTkFont(size=15), command=self.experiment1_switch_click)
        self.experiment1_switch.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        self.experiment2_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 2', font=customtkinter.CTkFont(size=15), command=self.experiment2_switch_click)
        self.experiment2_switch.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")

        self.experiment3_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 3', font=customtkinter.CTkFont(size=15), command=self.experiment3_switch_click)
        self.experiment3_switch.grid(row=3, column=0, pady=10, padx=20, sticky="nsew")

        self.experiment4_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 3', font=customtkinter.CTkFont(size=15), command=self.experiment4_switch_click)
        self.experiment4_switch.grid(row=4, column=0, pady=10, padx=20, sticky="nsew")

        self.experiment5_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 3', font=customtkinter.CTkFont(size=15), command=self.experiment5_switch_click)
        self.experiment5_switch.grid(row=5, column=0, pady=10, padx=20, sticky="nsew")


        self.create_own_exp_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Create your own:', font=customtkinter.CTkFont(size=15), command=self.create_own_experiment)
        self.create_own_exp_switch.grid(row=6, column=0, pady=10, padx=20, sticky="nsew")

        """ Setup Generate Button """

        # Generate Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate)
        self.generate_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    def experiment1_switch_click(self) -> None:
        self.experiment2_switch.deselect()
        self.experiment3_switch.deselect()
        self.experiment4_switch.deselect()
        self.experiment5_switch.deselect()
        self.create_own_exp_switch.deselect()

    def experiment2_switch_click(self) -> None:
        self.experiment1_switch.deselect()
        self.experiment3_switch.deselect()
        self.experiment4_switch.deselect()
        self.experiment5_switch.deselect()
        self.create_own_exp_switch.deselect()

    def experiment3_switch_click(self) -> None:
        self.experiment1_switch.deselect()
        self.experiment2_switch.deselect()
        self.experiment4_switch.deselect()
        self.experiment5_switch.deselect()
        self.create_own_exp_switch.deselect()

    def experiment4_switch_click(self) -> None:
        self.experiment1_switch.deselect()
        self.experiment2_switch.deselect()
        self.experiment3_switch.deselect()
        self.experiment5_switch.deselect()
        self.create_own_exp_switch.deselect()

    def experiment5_switch_click(self) -> None:
        self.experiment1_switch.deselect()
        self.experiment2_switch.deselect()
        self.experiment3_switch.deselect()
        self.experiment4_switch.deselect()
        self.create_own_exp_switch.deselect()

    def create_own_experiment(self):

        state_own = self.create_own_exp_switch.get()
        if state_own:
            self.experiment1_switch.deselect()
            self.experiment2_switch.deselect()
            self.experiment3_switch.deselect()
            self.experiment4_switch.deselect()
            self.experiment5_switch.deselect()

            self.expand_gui()
            self.create_own_exp_frame = customtkinter.CTkFrame(self)
            self.create_own_exp_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")
            self.create_own_exp_frame.grid_columnconfigure(0, weight=1)
            self.create_own_exp_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

            self.label_initialization = customtkinter.CTkLabel(master=self.create_own_exp_frame, text="Choose settings:", font=customtkinter.CTkFont(size=15, weight='bold'))
            self.label_initialization.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

            self.greedy_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame, text='Greedy', font=customtkinter.CTkFont(size=15), command=self.greedy_switch_click)
            self.greedy_switch.grid(row=1, column=0, pady=10, padx=20, sticky="n")

            self.hill_climbing_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame, text='Hill Climbing', font=customtkinter.CTkFont(size=15), command=self.hillclimber_switch_click)
            self.hill_climbing_switch.grid(row=6, column=0, pady=10, padx=20, sticky="n")

            self.generate_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        else:

            self.hill_climbing_switch.destroy()

            try:
                self.annealing_switch.destroy()
            except:
                pass

            self.greedy_switch.deselect()

            try:
                self.greedy_switch_click()
            except:
                pass

            self.label_initialization.destroy()
            self.greedy_switch.destroy()

            self.collaps_gui()
            self.create_own_exp_frame.destroy()
            self.generate_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    def expand_gui(self):
        self.geometry(f"{500}x{450}")

    def expand_gui_greedy(self):
        self.geometry(f'{500}x{550}')

    def expand_gui_hilli(self):
        self.geometry(f'{500}x{550}')

    def collaps_gui(self):
        self.geometry(f'{250}x{450}')

    def run(self) -> None:
        self.mainloop()

    def hillclimber_switch_click(self) -> None:

        state_hc = self.hill_climbing_switch.get()

        if state_hc == 1:
            self.expand_gui_hilli()

            self.genetic_switch_solo = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Genetic', font=customtkinter.CTkFont(size=15), command=self.turn_of_pool)
            self.genetic_switch_solo.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

            self.genetic_switch_pool = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Genetic pooling', font=customtkinter.CTkFont(size=15), command=self.turn_of_an_solo)
            self.genetic_switch_pool.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

            self.annealing_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Sim. Annealing', font=customtkinter.CTkFont(size=15), command=self.turn_of_pool)
            self.annealing_switch.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

            self.iterations_dependend_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='iterations dependend', font=customtkinter.CTkFont(size=15), command=self.iterations_dependend)
            self.iterations_dependend_switch.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

            self.iterations_fixed_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Iterations fixed', font=customtkinter.CTkFont(size=15), command=self.iterations_fixed)
            self.iterations_fixed_switch.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")


        else:
            self.expand_gui_greedy()
            self.genetic_switch_solo.destroy()
            self.genetic_switch_pool.destroy()
            self.annealing_switch.destroy()

    def iterations_fixed(self):
        state = self.iterations_fixed_switch.get()
        if state:
            self.iterations1 = customtkinter.CTkEntry(master=self.create_own_exp_frame2, font=customtkinter.CTkFont(size=15))
            self.iterations1.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
            self.iterations_dependend_switch.deselect()
            try:
                self.iterations2.destroy()
            except:
                pass
        else:
            self.iterations1.destroy()

    def iterations_dependend(self):
        state = self.iterations_dependend_switch.get()
        if state:
            self.iterations2 = customtkinter.CTkEntry(master=self.create_own_exp_frame2, font=customtkinter.CTkFont(size=15))
            self.iterations2.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
            self.iterations_fixed_switch.deselect()
            try:
                self.iterations1.destroy()
            except:
                pass
        else:
            self.iterations2.destroy()


    def greedy_switch_click(self) -> None:
        

        state_greedy = self.greedy_switch.get()

        if state_greedy == 1:
            self.expand_gui_greedy()
            self.capacity_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Capacity', font=customtkinter.CTkFont(size=15))
            self.capacity_switch.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

            self.popular_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Popular first', font=customtkinter.CTkFont(size=15), command=self.turn_off_difficult_P)
            self.popular_switch.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

            self.popular_own_day_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Largest first', font=customtkinter.CTkFont(size=15), command=self.turn_off_difficult_POD)
            self.popular_own_day_switch.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

            self.difficult_students_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Busy Students', font=customtkinter.CTkFont(size=15), command=self.turn_off_popular)
            self.difficult_students_switch.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")


        else:
            self.expand_gui()
            self.capacity_switch.destroy()
            self.popular_switch.destroy()
            self.popular_own_day_switch.destroy()
            self.difficult_students_switch.destroy()

    def turn_of_pool(self):
        state1 = self.annealing_switch.get()
        state2 = self.genetic_switch_solo.get()
        if state1 or state2:
            self.genetic_switch_pool.deselect()

    def turn_of_an_solo(self):
        state1 = self.genetic_switch_pool.get()
        if state1:
            self.annealing_switch.deselect()
            self.genetic_switch_solo.deselect()

    def run_experiment(self):
        if self.experiment1_switch.get():
            self.run_exp_1()

    def run_exp_1(self) -> None:
        # Set setting for initialization plot or optimalization

        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        mode = 'multiproccesing'

        core_assignment = [0,0,2,2]

        hill_climber_iters = 50

        self.destroy()

        with open('data/experiment1.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([])

        for i in range(30):
            GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize,
                                     mode, core_assignment, hill_climber_iters, i)

        # Plot Funtion

        self.finish(student_list)


    def turn_off_difficult_POD(self) -> None:
        state_popular_own_day = self.popular_own_day_switch.get()
        if state_popular_own_day == 1:

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

        exp1 = self.experiment1_switch.get()
        exp2 = self.experiment2_switch.get()
        exp3 = self.experiment3_switch.get()
        exp4 = self.experiment4_switch.get()
        exp5 = self.experiment5_switch.get()
        own_exp = self.create_own_exp_switch.get()

        if exp1:
            self.run_exp_1()
        elif exp2:
            self.run_exp_2()
        elif exp3:
            self.run_exp_3()
        elif exp4:
            self.run_exp_4()
        elif exp5:
            self.run_exp_5()
        elif own_exp:

            # Extract state_data from GUI
            settings = self.__set_data()

            # Destroy window
            self.destroy()

            self.__run_algorithm(settings)

    def finish(self, student_list):

        with open('schedule.pkl', 'rb') as f:
            schedule = pickle.load(f)

        app = SelectorApp.App(student_list, schedule)
        app.mainloop()


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

    def __run_algorithm(self, settings) -> None:

        capacity, popular, popular_own_day, difficult_students, annealing, visualize = settings

        G = GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize)

        if not visualize:
            G.optimize()

    def __gen_core_assignment_list(self) -> list:
        core_arragments = []
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        core_arragments.append(f'{a}{b}{c}{d}')
        return core_arragments