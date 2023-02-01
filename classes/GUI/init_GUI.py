import customtkinter
import csv
import classes.algorithms.generator as GeneratorClass
import classes.GUI.selector_GUI as SelectorApp
from data.assign import student_list
import pickle

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        # set a starting height and width
        self.width = 250
        self.height = 450

        # configure window
        self.title("Scheduly")
        self.geometry(f"{self.width}x{self.height}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.init_gui()

    """ Init """

    def init_gui(self):
        """ Optimize Configure Frame """

        self.toggle_frame = customtkinter.CTkFrame(self)
        self.toggle_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        self.toggle_frame.grid_columnconfigure(0, weight=1)
        self.toggle_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        self.label_experiment = customtkinter.CTkLabel(master=self.toggle_frame, text="Experiments:", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_experiment.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.buttons = []
        self.experiment1_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 1', font=customtkinter.CTkFont(size=15), command=lambda:self.toggle_buttons(0))
        self.experiment1_switch.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
        self.buttons.append(self.experiment1_switch)

        self.experiment2_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 2', font=customtkinter.CTkFont(size=15), command=lambda: self.toggle_buttons(1))
        self.experiment2_switch.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.buttons.append(self.experiment2_switch)

        

        self.experiment3_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 3', font=customtkinter.CTkFont(size=15), command=lambda:self.toggle_buttons(2))
        self.experiment3_switch.grid(row=3, column=0, pady=10, padx=20, sticky="nsew")
        self.buttons.append(self.experiment3_switch)


        self.experiment4_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 4', font=customtkinter.CTkFont(size=15), command=lambda:self.toggle_buttons(3))
        self.experiment4_switch.grid(row=4, column=0, pady=10, padx=20, sticky="nsew")
        self.buttons.append(self.experiment4_switch)


        self.experiment5_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 5', font=customtkinter.CTkFont(size=15), command=lambda:self.toggle_buttons(4))
        self.experiment5_switch.grid(row=5, column=0, pady=10, padx=20, sticky="nsew")
        self.buttons.append(self.experiment5_switch)


        self.create_own_exp_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Create your own:', font=customtkinter.CTkFont(size=15), command=self.create_own_experiment)
        self.create_own_exp_switch.grid(row=6, column=0, pady=10, padx=20, sticky="nsew")
        self.buttons.append(self.create_own_exp_switch)


        """ Setup Generate Button """

        # Generate Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate)
        self.generate_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    """ Toggle switches """
    def toggle_buttons(self, i):
        '''
        Method goes over all the experiments buttons and deselects every button that does not correspond to the
        input integer connected to a specific button. Adjusts the GUI frame if necessary with the try-except statement
        '''
        for _, button in enumerate(self.buttons):
            if _ != i:
                button.deselect()
                try: 
                    self.create_own_exp_frame1.destroy()
                    self.create_own_exp_frame2.destroy()
                except:
                    pass
                self.width = 250
                self.height = 450
                self.geometry(f"{self.width}x{self.height}")

    def create_own_experiment(self):
        '''
        Method expands the GUI when users want to create their own experiment. Also collapses the GUI by calling the toggle_button
        '''

        # check if activated
        state_own = self.create_own_exp_switch.get()
        if state_own:

            # disable other experiment buttons
            self.toggle_buttons(5)

            # expand GUI
            self.width += 500
            self.geometry(f"{self.width}x{self.height}")

            self.create_own_exp_frame1 = customtkinter.CTkFrame(self)
            self.create_own_exp_frame1.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            self.create_own_exp_frame1.grid_columnconfigure(0, weight=1)
            self.create_own_exp_frame1.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

            self.create_own_exp_frame2 = customtkinter.CTkFrame(self)
            self.create_own_exp_frame2.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
            self.create_own_exp_frame2.grid_columnconfigure(0, weight=1)
            self.create_own_exp_frame2.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

            # create labels 
            self.label_initialization = customtkinter.CTkLabel(master=self.create_own_exp_frame1, text="Choose settings:", font=customtkinter.CTkFont(size=15, weight='bold'))
            self.label_initialization.grid(row=0, column=0, padx=20, pady=10, sticky="ns")
            self.label_initialization = customtkinter.CTkLabel(master=self.create_own_exp_frame2, text="Choose settings:", font=customtkinter.CTkFont(size=15, weight='bold'))
            self.label_initialization.grid(row=0, column=1, padx=20, pady=10, sticky="ns")

            # initiate the heuristic menu if clicked
            self.heuristick_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Heuristics:', font=customtkinter.CTkFont(size=15), command=self.heuristick_switch_click)
            self.heuristick_switch.grid(row=1, column=0, pady=10, padx=20, sticky="n")

            # initiate the algorithm menu if clicked
            self.algorithm_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Algorithms:', font=customtkinter.CTkFont(size=15), command=self.algorithm_switch_click)
            self.algorithm_switch.grid(row=1, column=0, columnspan=4, pady=10, padx=20, sticky="n")
        else:

            self.toggle_buttons(6)


    def heuristick_switch_click(self) -> None:
        '''
        Drops down a menu in the GUI where the user can select heuristics to influence the initialisation
        of the schedule
        '''

        # check its state
        state_greedy = self.heuristick_switch.get()
        if state_greedy == 1:

            # resize and create switches
            self.width += 20

            self.geometry(f"{self.width}x{self.height}")
            self.heursistic_buttons = []
            self.capacity_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Capacity', font=customtkinter.CTkFont(size=15))
            self.capacity_switch.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
            self.popular_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Popular first', font=customtkinter.CTkFont(size=15), command=lambda: self.turn_of_heuristics(1))
            self.popular_switch.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
            self.popular_own_day_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Largest first', font=customtkinter.CTkFont(size=15), command=lambda: self.turn_of_heuristics(2))
            self.popular_own_day_switch.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
            self.difficult_students_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Busy Students', font=customtkinter.CTkFont(size=15), command=lambda: self.turn_of_heuristics(3))
            self.difficult_students_switch.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
            self.heursistic_buttons.append(self.popular_switch)
            self.heursistic_buttons.append(self.popular_own_day_switch)
            self.heursistic_buttons.append(self.difficult_students_switch)

        else:
            # destroy its content when turned of and resize
            self.width -= 20
            self.geometry(f"{self.width}x{self.height}")
            self.capacity_switch.destroy()
            self.popular_switch.destroy()
            self.popular_own_day_switch.destroy()
            self.difficult_students_switch.destroy()

    def turn_of_heuristics(self, i):
        if i != 3:
            self.heursistic_buttons[2].deselect()
        else:
            for ii in range(2):
                self.heursistic_buttons[ii].deselect()

    def algorithm_switch_click(self) -> None:
        '''
        Method drops down a menu to select what type of algorithm user wants to use. Consult README on git 
        for more details about what each option does
        '''

        # check the state
        state_hc = self.algorithm_switch.get()

        if state_hc == 1:
            # expand the GUI
            self.width += 200
            self.height += 100
            self.geometry(f"{self.width}x{self.height}")

            # create the buttons for algorithm selection options
            self.hillclimber_multi = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Hilclimber multiple cores', font=customtkinter.CTkFont(size=15), command=self.hilli_multi)
            self.hillclimber_multi.grid(row=2, column=0, padx=20, columnspan=4, pady=10, sticky="nsew")

            self.hillclimber_single = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Hilclimber single cores', font=customtkinter.CTkFont(size=15), command=self.hilli_single)
            self.hillclimber_single.grid(row=3, column=0, padx=20, columnspan=4, pady=10, sticky="nsew")

            self.genetic_switch_solo = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Genetic', font=customtkinter.CTkFont(size=15), command=self.genni_single)
            self.genetic_switch_solo.grid(row=5, column=0, padx=20, columnspan=4, pady=10, sticky="nsew")

            self.genetic_switch_pool = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Genetic pooling', font=customtkinter.CTkFont(size=15), command=self.genni_multi)
            self.genetic_switch_pool.grid(row=4, column=0, padx=20, columnspan=4, pady=10, sticky="nsew")

            self.iterations_dependend_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='iterations dependend', font=customtkinter.CTkFont(size=15), command=self.iterations_dependend)
            self.iterations_dependend_switch.grid(row=7, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

            self.iterations_fixed_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Iterations fixed', font=customtkinter.CTkFont(size=15), command=self.iterations_fixed)
            self.iterations_fixed_switch.grid(row=9, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

            self.duration_box = customtkinter.CTkComboBox(self.create_own_exp_frame2, values=["1", "5", "10", "15", "30", "45", "60", "120", "180"])
            self.duration_box.grid(row=11, column=0, padx=20, columnspan=4, pady=10, sticky="nsew")
            self.duration_box.set("Duration (Mins.)")


            # create a pop up menu
            self.hillclimber_assignment = customtkinter.CTkButton(self.create_own_exp_frame2, text="Choose Hillclimbers", command=self.open_input_window)
            self.hillclimber_assignment.place(relx=0.5, rely=0.5, anchor='center')
            self.hillclimber_assignment.grid(row=12, column=0, padx=20, pady=10, sticky="nsew")


        else:
            # collaps GUI
            self.width -= 200
            self.height -= 100

            self.geometry(f"{self.width}x{self.height}")
            self.genetic_switch_solo.destroy()
            self.genetic_switch_pool.destroy()
            try: # cannot destroy items that are not present, so unfortunately try-except are needed
                self.annealing_switch.destroy()
            except:
                pass
            try:
                self.iterations1.destroy()
            except:
                pass
            try:
                self.iterations2.destroy()
            except:
                pass
            self.iterations_dependend_switch.destroy()
            self.iterations_fixed_switch.destroy()
            self.duration_box.destroy()
            self.hillclimber_assignment.destroy()
            self.hillclimber_multi.destroy()
            self.hillclimber_single.destroy()

    def hilli_multi(self):
        '''
        method that deselects options that are not compatible with hillclimber
        '''
        if self.hillclimber_multi.get():
            self.hillclimber_single.deselect()
            self.genetic_switch_pool.deselect()
            self.genetic_switch_solo.deselect()
            try:
                self.annealing_switch.destroy()
            except:
                pass

    def hilli_single(self):
        '''
        method that deselects options that are not compatible with hillclimber
        '''
        if self.hillclimber_single.get():
            self.hillclimber_multi.deselect()
            self.genetic_switch_pool.deselect()
            self.genetic_switch_solo.deselect()
            try:
                self.annealing_switch.destroy()
            except:
                pass

    def genni_single(self):
        '''
        method that deselects options that are not compatible with genetic algorithm
        '''
        if self.genetic_switch_solo.get():

            # update GUI size
            self.height += 50
            self.geometry(f"{self.width}x{self.height}")

            # create an annealing switch
            self.annealing_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Sim. Annealing', font=customtkinter.CTkFont(size=15), command=self.simmi_an)
            self.annealing_switch.grid(row=6, column=0, padx=20, columnspan=4, pady=10, sticky="nsew")
            self.genetic_switch_pool.deselect()
            self.hillclimber_single.deselect()
            self.hillclimber_multi.deselect()
        else:
            # collaps GUI
            self.height -= 50
            self.geometry(f"{self.width}x{self.height}")
            try: # if there is an annealing switch, destroy
                self.annealing_switch.destroy()
            except:
                pass

    def genni_multi(self):
        '''
        method that deselects options that are not compatible with genetic multiple cores algorithm
        '''
        if self.genetic_switch_pool.get():
            self.genetic_switch_solo.deselect()
            self.hillclimber_single.deselect()
            self.hillclimber_multi.deselect()
        try:
            self.annealing_switch.destroy()
        except:
            pass

    def simmi_an(self):
        '''
        method that updates the simulated annealing
        '''
        if not self.genetic_switch_solo.get():
            self.annealing_switch.deselect()
        elif self.annealing_switch.get():
            self.hillclimber_single.deselect()
            self.hillclimber_multi.deselect()
            self.genetic_switch_pool.deselect()


    """ Interacting functions """

    def iterations_fixed(self):
        state = self.iterations_fixed_switch.get()
        if state:
            if not self.iterations_dependend_switch.get():
                self.height += 75

            self.geometry(f"{self.width}x{self.height}")
            self.iterations1 = customtkinter.CTkEntry(master=self.create_own_exp_frame2, font=customtkinter.CTkFont(size=15))
            self.iterations1.grid(row=10, column=0, padx=20, pady=10, sticky="nsew")
            self.iterations_dependend_switch.deselect()
            try:
                self.iterations2.destroy()
            except:
                pass
        else:
            self.height -= 75
            self.geometry(f"{self.width}x{self.height}")
            self.iterations1.destroy()

    def iterations_dependend(self):
        state = self.iterations_dependend_switch.get()
        if state:
            if not self.iterations_fixed_switch.get():
                self.height += 75

            self.geometry(f"{self.width}x{self.height}")
            self.iterations2 = customtkinter.CTkEntry(master=self.create_own_exp_frame2, font=customtkinter.CTkFont(size=15))
            self.iterations2.grid(row=8, column=0, padx=20, pady=10, sticky="nsew")

            self.iterations_fixed_switch.deselect()
            try:
                self.iterations1.destroy()
            except:
                pass
        else:

            self.height -= 75
            self.geometry(f"{self.width}x{self.height}")
            self.iterations2.destroy()

    def open_input_window(self):
        dialog = customtkinter.CTkInputDialog(text="Please enter 4 digits from 0 to 3\nDefault: 0123", title="Hillclimbers")
        self.hillclimber_assignment = dialog.get_input()

    """ Run functions """

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

            self.__run_algorithm(settings)

    def run_exp_1(self) -> None:

        # Set setting for initialization plot or optimalization

        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        experiment = 1

        duration = 15 * 60

        mode = 'multiproccesing'

        hillclimber_assignment = [0,0,2,2]

        hill_climber_iters = 50

        # Destroy GUI window
        self.destroy()

        self.__reset_data_file(experiment)

        for i in range(30):
            G = GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize)
            G.optimize(experiment, mode, hillclimber_assignment, hill_climber_iters, duration, i)

        # Plot Funtion

        self.finish(student_list)

    def run_exp_2(self) -> None:
        # Set setting for initialization plot or optimalization

        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        experiment = 2

        duration = 15 * 60

        mode = 'multiproccesing'

        hillclimber_assignment = [0,0,0,0]

        hill_climber_iters = 50

        self.destroy()

        self.__reset_data_file(experiment)

        for i in range(30):
            G = GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize)
            G.optimize(experiment, mode, hillclimber_assignment, hill_climber_iters, duration, i)
        # Plot Funtion

        self.finish(student_list)

    def run_exp_3(self) -> None:
        # Set setting for initialization plot or optimalization

        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        experiment = 3

        duration = 15 * 60

        mode = 'multiproccesing'

        hillclimber_assignment = [2,2,2,2]

        hill_climber_iters = 50

        self.destroy()

        self.__reset_data_file(experiment)

        for i in range(30):
            G = GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize)
            G.optimize(experiment, mode, hillclimber_assignment, hill_climber_iters, duration, i)
        # Plot Funtion

        self.finish(student_list)

    def run_exp_4(self) -> None:
        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        experiment = 4

        duration = 15 * 60

        mode = 'multiproccesing'

        hillclimber_assignment = [2,2,2,2]

        hill_climber_iters = 0.1

        self.__reset_data_file(experiment)

        self.destroy()

        G = GeneratorClass.Generator(capacity, popular, popular_own_day,
                                    difficult_students, annealing, visualize)
        G.optimize(experiment, mode, hillclimber_assignment, hill_climber_iters, duration)
        # Plot Funtion

        self.finish(student_list)

        for i, hill_climber_iters in enumerate[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
            G = GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize)
            G.optimize(experiment, mode, hillclimber_assignment, hill_climber_iters, duration, i)
        # Plot Funtion

        self.finish(student_list)

    def run_exp_5(self) -> None:
        capacity = False

        popular = False

        popular_own_day = False

        difficult_students = False

        annealing = False

        visualize = False

        duration = 15 * 60

        experiment = 4

        mode = 'genetic pool'

        hillclimber_assignment = [0,0,2,2]

        hill_climber_iters = 400

        self.__reset_data_file(experiment)

        self.destroy()

        for i in range(30):
            G = GeneratorClass.Generator(capacity, popular, popular_own_day,
                                     difficult_students, annealing, visualize)
            G.optimize(experiment, mode, hillclimber_assignment, hill_climber_iters, duration, i)
        

        self.finish(student_list)

    """ Methods """

    def run(self) -> None:
        self.mainloop()

    def finish(self, student_list) -> None:

        with open('schedule.pkl', 'rb') as f:
            schedule = pickle.load(f)

        app = SelectorApp.App(student_list, schedule)
        app.mainloop()

    """ Helpers """

    def __reset_data_file(self, experiment) -> None:
        with open(f'data/experiment{experiment}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([])

    def __set_data(self) -> tuple:

        # Collect state of hill climbing switch
        algorithm = self.algorithm_switch.get()

        # Set setting for initialization plot or optimalization
        if algorithm:
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

        if not visualize:
            try:
                duration = int(self.duration_box.get()) * 60
            except:
                return

            if self.iterations_fixed_switch.get():
                try:
                    iterations = int(self.iterations1.get())
                except:
                    return
            elif self.iterations_dependend_switch.get():
                try:
                    iterations = float(self.iterations2.get())
                except:
                    return
            else:
                return

            if self.hillclimber_single.get():
                mode = 'sequential'
            elif self.hillclimber_multi.get():
                mode = 'multiproccesing'
            elif self.genetic_switch_solo.get():
                mode = 'genetic'
            elif self.genetic_switch_pool.get():
                mode = 'genetic pool'
            else:
                return

        hillclimber_assignment = []
        try:
            if len(self.hillclimber_assignment) < 4:
                hillclimber_assignment = [0,1,2,3]
            else:
                for digit in self.hillclimber_assignment:
                    hillclimber_assignment.append(int(digit))
        except:
            hillclimber_assignment = [0,1,2,3]

        print('The Hillclimbers you selected are:')
        print(hillclimber_assignment)

        # Destroy window
        self.destroy()

        experiment = 0

        self.__reset_data_file(experiment)

        G = GeneratorClass.Generator(capacity, popular, popular_own_day,
                                    difficult_students, annealing, visualize)
        if not visualize:

            # Set the hill climber iterations
            hill_climber_iters = iterations

            # Run the optimize function
            G.optimize(experiment, mode, hillclimber_assignment, hill_climber_iters, duration)
            # Plot Funtion

            self.finish(student_list)

        self.mainloop()