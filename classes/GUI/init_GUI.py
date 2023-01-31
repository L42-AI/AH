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
        self.geometry(f"{250}x{350}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        """ Optimize Configure Frame """
        
        self.toggle_frame = customtkinter.CTkFrame(self)
        self.toggle_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        self.toggle_frame.grid_columnconfigure(0, weight=1)
        self.toggle_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)
    
        

        self.label_experiment = customtkinter.CTkLabel(master=self.toggle_frame, text="Experiments:", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_experiment.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.experiment1_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 1', font=customtkinter.CTkFont(size=15))
        self.experiment1_switch.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        self.experiment2_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 2', font=customtkinter.CTkFont(size=15))
        self.experiment2_switch.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        
        self.experiment3_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 3', font=customtkinter.CTkFont(size=15))
        self.experiment3_switch.grid(row=3, column=0, pady=10, padx=20, sticky="nsew")

        self.create_own_exp_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Create your own:', font=customtkinter.CTkFont(size=15), command=self.create_own_experiment)
        self.create_own_exp_switch.grid(row=4, column=0, pady=10, padx=20, sticky="nsew")
        
        

        """ Setup Generate Button """

        # Generate Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate)
        self.generate_button.grid(row=8, column=0, padx=20, pady=10, sticky="ew")

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
            self.create_own_exp_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            self.create_own_exp_frame.grid_columnconfigure(0, weight=1)
            self.create_own_exp_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)
            self.label_initialization = customtkinter.CTkLabel(master=self.create_own_exp_frame, text="Choose settings:", font=customtkinter.CTkFont(size=15, weight='bold'))
            self.label_initialization.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

            self.greedy_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame, text='Greedy', font=customtkinter.CTkFont(size=15), command=self.greedy_switch_click)
            self.greedy_switch.grid(row=1, column=0, pady=10, padx=20, sticky="n")

            self.hill_climbing_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame, text='Hill Climbing', font=customtkinter.CTkFont(size=15), command=self.hillclimber_switch_click)
            self.hill_climbing_switch.grid(row=6, column=0, pady=10, padx=20, sticky="n")
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

    def expand_gui(self):
        self.geometry(f"{500}x{550}")

    def expand_gui_greedy(self):
        self.geometry(f'{500}x{550}')

    def expand_gui_hilli(self):
        self.geometry(f'{500}x{650}')

    def collaps_gui(self):
        self.geometry(f'{250}x{350}')

    def run(self) -> None:
        self.mainloop()

    def hillclimber_switch_click(self) -> None:

        state_hc = self.hill_climbing_switch.get()

        if state_hc == 1:
            self.expand_gui_hilli()
            self.annealing_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame, text='Sim. Annealing', font=customtkinter.CTkFont(size=15))
            self.annealing_switch.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        else:
            self.expand_gui_greedy()
            self.annealing_switch.destroy()

    def greedy_switch_click(self) -> None:
        

        state_greedy = self.greedy_switch.get()

        if state_greedy == 1:
            self.expand_gui_greedy()
            self.capacity_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame, text='Capacity', font=customtkinter.CTkFont(size=15))
            self.capacity_switch.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

            self.popular_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame, text='Popular first', font=customtkinter.CTkFont(size=15), command=self.turn_off_difficult_P)
            self.popular_switch.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

            self.popular_own_day_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame, text='Largest first', font=customtkinter.CTkFont(size=15), command=self.turn_off_difficult_POD)
            self.popular_own_day_switch.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

            self.difficult_students_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame, text='Busy Students', font=customtkinter.CTkFont(size=15), command=self.turn_off_popular)
            self.difficult_students_switch.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

        else:
            self.expand_gui()
            self.capacity_switch.destroy()
            self.popular_switch.destroy()
            self.popular_own_day_switch.destroy()
            self.difficult_students_switch.destroy()

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

        experiment = 1

        mode = 'multiproccesing'

        core_assignment = [0,0,2,2]

        hill_climber_iters = 50

        self.destroy()

        self.__reset_data_file(experiment)

        for i in range(30):
            GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize,
                                     experiment, mode, core_assignment,
                                     hill_climber_iters, i)
        # Plot Funtion

    def experiment2_switch_click(self) -> None:
        # Set setting for initialization plot or optimalization

        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        experiment = 2

        mode = 'multiproccesing'

        core_assignment = [0,0,0,0]

        hill_climber_iters = 50

        self.destroy()

        self.__reset_data_file(experiment)

        for i in range(30):
            GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize,
                                     experiment, mode, core_assignment,
                                     hill_climber_iters, i)
        # Plot Funtion

    def experiment3_switch_click(self) -> None:
        # Set setting for initialization plot or optimalization

        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        experiment = 3

        mode = 'multiproccesing'

        core_assignment = [2,2,2,2]

        hill_climber_iters = 50

        self.destroy()

        self.__reset_data_file(experiment)

        for i in range(30):
            GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize,
                                     experiment, mode, core_assignment,
                                     hill_climber_iters, i)
        # Plot Funtion

    def experiment4_switch_click(self) -> None:
        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        experiment = 4

        mode = 'multiproccesing'

        core_assignment = [2,2,2,2]

        hill_climber_iters = 0.1

        self.__reset_data_file(experiment)

        GeneratorClass.Generator(capacity, popular, popular_own_day,
                                    difficult_students, annealing, visualize,
                                    experiment, mode, core_assignment,
                                    hill_climber_iters, 1)

        for i, hill_climber_iters in enumerate[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
            GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize,
                                     experiment, mode, core_assignment,
                                     hill_climber_iters, i)

    def experiment5_switch_click(self) -> None:
        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        experiment = 4

        mode = 'genetic pool'

        core_assignment = [0,0,2,2]

        hill_climber_iters = 400

        self.__reset_data_file(experiment)

        for i in range(30):
            GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize,
                                     experiment, mode, core_assignment,
                                     hill_climber_iters, i)

    def __reset_data_file(self, experiment) -> None:
        with open(f'data/experiment{experiment}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([])


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
