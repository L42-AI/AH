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
       
        self.width = 250
        self.height = 450

        # configure window
        self.title("Scheduly")
        self.geometry(f"{self.width}x{self.height}")

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

        self.experiment4_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 4', font=customtkinter.CTkFont(size=15), command=self.experiment4_switch_click)
        self.experiment4_switch.grid(row=4, column=0, pady=10, padx=20, sticky="nsew")

        self.experiment5_switch = customtkinter.CTkCheckBox(master=self.toggle_frame, text='Experiment 5', font=customtkinter.CTkFont(size=15), command=self.experiment5_switch_click)
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

            self.label_initialization = customtkinter.CTkLabel(master=self.create_own_exp_frame1, text="Choose settings:", font=customtkinter.CTkFont(size=15, weight='bold'))
            self.label_initialization.grid(row=0, column=0, padx=20, pady=10, sticky="ns")
            self.label_initialization = customtkinter.CTkLabel(master=self.create_own_exp_frame2, text="Choose settings:", font=customtkinter.CTkFont(size=15, weight='bold'))
            self.label_initialization.grid(row=0, column=1, padx=20, pady=10, sticky="ns")

            self.greedy_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Initialise:', font=customtkinter.CTkFont(size=15), command=self.greedy_switch_click)
            self.greedy_switch.grid(row=1, column=0, pady=10, padx=20, sticky="n")

            self.hill_climbing_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Optimize:', font=customtkinter.CTkFont(size=15), command=self.hillclimber_switch_click)
            self.hill_climbing_switch.grid(row=1, column=0, columnspan=4, pady=10, padx=20, sticky="n")
        else:

            self.width -= 500
            self.geometry(f"{self.width}x{self.height}")

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

            self.create_own_exp_frame1.destroy()
            self.create_own_exp_frame2.destroy()


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


    def hilli_multi(self):
        if self.hillclimber_multi.get():
            self.hillclimber_single.deselect()
            self.genetic_switch_pool.deselect()
            self.genetic_switch_solo.deselect()
            try:
                self.annealing_switch.destroy()
            except:
                pass

    def hilli_single(self):
        if self.hillclimber_single.get():
            self.hillclimber_multi.deselect()
            self.genetic_switch_pool.deselect()
            self.genetic_switch_solo.deselect()
            try:
                self.annealing_switch.destroy()
            except:
                pass

    def genni_single(self):
        if self.genetic_switch_solo.get():
            self.height += 50

            self.geometry(f"{self.width}x{self.height}")
            self.annealing_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame2, text='Sim. Annealing', font=customtkinter.CTkFont(size=15), command=self.simmi_an)
            self.annealing_switch.grid(row=6, column=0, padx=20, columnspan=4, pady=10, sticky="nsew")
            self.genetic_switch_pool.deselect()
            self.hillclimber_single.deselect()
            self.hillclimber_multi.deselect()
        else:
            self.height -= 50

            self.geometry(f"{self.width}x{self.height}")
            try:
                self.annealing_switch.destroy()
            except:
                pass

    def genni_multi(self):
        if self.genetic_switch_pool.get():
            self.genetic_switch_solo.deselect()
            self.hillclimber_single.deselect()
            self.hillclimber_multi.deselect()
        try:
            self.annealing_switch.destroy()
        except:
            pass

    def simmi_an(self):
        if not self.genetic_switch_solo.get():
            self.annealing_switch.deselect()
        elif self.annealing_switch.get():
            self.hillclimber_single.deselect()
            self.hillclimber_multi.deselect()
            self.genetic_switch_pool.deselect()

    def button_click_event(self):
        dialog = customtkinter.CTkInputDialog(text="Please enter 4 digits from 0 to 3\nDefault: 0123", title="Hillclimbers")
        self.hillclimber_assignment = dialog.get_input()


    def hillclimber_switch_click(self) -> None:

        state_hc = self.hill_climbing_switch.get()

        if state_hc == 1:
            self.width += 200
            self.height += 100

            self.geometry(f"{self.width}x{self.height}")
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
            self.hillclimber_assignment = customtkinter.CTkButton(self.create_own_exp_frame2, text="Choose Hillclimbers", command=self.button_click_event)
            self.hillclimber_assignment.place(relx=0.5, rely=0.5, anchor='center')
            self.hillclimber_assignment.grid(row=12, column=0, padx=20, pady=10, sticky="nsew")


        else:
            self.width -= 200
            self.height -= 100

            self.geometry(f"{self.width}x{self.height}")
            self.genetic_switch_solo.destroy()
            self.genetic_switch_pool.destroy()
            try:
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

    def greedy_switch_click(self) -> None:

        state_greedy = self.greedy_switch.get()

        if state_greedy == 1:
            self.width += 20

            self.geometry(f"{self.width}x{self.height}")
            self.capacity_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Capacity', font=customtkinter.CTkFont(size=15))
            self.capacity_switch.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

            self.popular_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Popular first', font=customtkinter.CTkFont(size=15), command=self.turn_off_difficult_P)
            self.popular_switch.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

            self.popular_own_day_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Largest first', font=customtkinter.CTkFont(size=15), command=self.turn_off_difficult_POD)
            self.popular_own_day_switch.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

            self.difficult_students_switch = customtkinter.CTkSwitch(master=self.create_own_exp_frame1, text='Busy Students', font=customtkinter.CTkFont(size=15), command=self.turn_off_popular)
            self.difficult_students_switch.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

        else:
            self.width -= 20

            self.geometry(f"{self.width}x{self.height}")

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
        # Plot Funtion

        self.finish(student_list)


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

            self.__run_algorithm(settings)

    def finish(self, student_list):

        with open('schedule.pkl', 'rb') as f:
            schedule = pickle.load(f)

        app = SelectorApp.App(student_list, schedule)
        app.mainloop()


    def run(self) -> None:
        self.mainloop()


    def __reset_data_file(self, experiment) -> None:
        with open(f'data/experiment{experiment}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([])

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

        hill_climber_iters = iterations

        self.__reset_data_file(experiment)

        G = GeneratorClass.Generator(capacity, popular, popular_own_day,
                                    difficult_students, annealing, visualize)
        if not visualize:
            G.optimize(experiment, mode, hillclimber_assignment, hill_climber_iters, duration)
            # Plot Funtion

            self.finish(student_list)

        core_arragments = []
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        core_arragments.append(f'{a}{b}{c}{d}')
        return core_arragments