import tkinter
import tkinter.messagebox
import customtkinter

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

        self.switch_1 = customtkinter.CTkSwitch(master=self.toggle_frame, text='Greedy', font=customtkinter.CTkFont(size=13))
        self.switch_1.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.switch_2 = customtkinter.CTkSwitch(master=self.toggle_frame, text='Hill Climber', font=customtkinter.CTkFont(size=13))
        self.switch_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.switch_3 = customtkinter.CTkSwitch(master=self.toggle_frame, text='Sim. Annealing', font=customtkinter.CTkFont(size=13))
        self.switch_3.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.label_methods_group = customtkinter.CTkLabel(master=self.toggle_frame, text="Methods", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_methods_group.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.switch_4 = customtkinter.CTkSwitch(master=self.toggle_frame, text='Classes Swap', font=customtkinter.CTkFont(size=13))
        self.switch_4.grid(row=5, column=0, pady=10, padx=20, sticky="n")
        self.switch_5 = customtkinter.CTkSwitch(master=self.toggle_frame, text='Student Swap', font=customtkinter.CTkFont(size=13))
        self.switch_5.grid(row=6, column=0, pady=10, padx=20, sticky="n")

        """ Setup Multiprocessing Button """

        # Parallel option
        self.parallel_frame = customtkinter.CTkFrame(self)
        self.parallel_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.parallel_frame.grid_columnconfigure(0, weight=1)
        self.parallel_frame.grid_rowconfigure(0, weight=1)

        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.parallel_frame, text='Multiprocessing', font=customtkinter.CTkFont(size=15, weight='bold'))
        self.checkbox_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        """ Setup Generate Button """

        # Generate Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate)
        self.generate_button.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        # Generate Optimal Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate Optimal", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate)
        self.generate_button.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")


        # """ Malus Configure Frame """

        # self.init_frame = customtkinter.CTkFrame(self)
        # self.init_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="new")
        # self.init_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # self.init_text = customtkinter.CTkLabel(master=self.init_frame, text="Create Your Schedule", font=customtkinter.CTkFont(size=17, weight='bold'))
        # self.init_text.grid(row=0, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")


        # self.switch_frame = customtkinter.CTkFrame(self)
        # self.switch_frame.grid(row=0, column=2, padx=20, pady=20, sticky="new")
        # self.switch_frame.grid_columnconfigure(0, weight=1)

        # self.switch_state = 0

        # self.malus_switch = customtkinter.CTkCheckBox(master=self.switch_frame, text="Configure Malus", font=customtkinter.CTkFont(size=15, weight='bold'), command=lambda: self.toggle_malus_slider(self.switch_state))
        # self.malus_switch.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        # """ Malus Configure Sliders """

        # self.malus_slider_frame = customtkinter.CTkFrame(self)

        # self.label_slider_1 = customtkinter.CTkLabel(master=self.malus_slider_frame, text="Gap Hours", font=customtkinter.CTkFont(size=15, weight='bold'))
        # self.label_slider_1.grid(row=0, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

        # self.slider_1 = customtkinter.CTkSlider(self.malus_slider_frame, from_=0.1, to=3, number_of_steps=15, command=self.update_malus_1)
        # self.slider_1.grid(row=1, column=0, columnspan=6, padx=20, pady=20, sticky="sew")

        # self.label_var_1 = tkinter.StringVar(value=1)

        # self.slider_1_number = customtkinter.CTkLabel(master=self.malus_slider_frame, textvariable=self.label_var_1, font=customtkinter.CTkFont(size=15, weight='bold'))
        # self.slider_1_number.grid(row=1, column=7, padx=20, pady=20, sticky="ew")


        # self.label_slider_2 = customtkinter.CTkLabel(master=self.malus_slider_frame, text="Night Classes", font=customtkinter.CTkFont(size=15, weight='bold'))
        # self.label_slider_2.grid(row=2, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

        # self.slider_2 = customtkinter.CTkSlider(self.malus_slider_frame, from_=0.1, to=3, number_of_steps=15, command=self.update_malus_2)
        # self.slider_2.grid(row=3, column=0, columnspan=6, padx=20, pady=20, sticky="sew")

        # self.label_var_2 = tkinter.StringVar(value=1)

        # self.slider_2_number = customtkinter.CTkLabel(master=self.malus_slider_frame, textvariable=self.label_var_2, font=customtkinter.CTkFont(size=15, weight='bold'))
        # self.slider_2_number.grid(row=3, column=7, padx=20, pady=20, sticky="ew")


    def generate(self):
        pass


    def toggle_malus_slider(self, state):

        # If the input checkbox is off:
        if state == 0:

            # Alternate the state
            self.switch_state = 1

            self.malus_slider_frame.grid(row=1, column=0, rowspan=4, columnspan=3, padx=20, pady=20, sticky="sew")
            self.malus_slider_frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)
        else:
            # Alternate the state
            self.switch_state = 0

            self.malus_slider_frame.grid_remove()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def update_malus_1(self, value):
        self.label_var_1.set(round(value,1))
        print('yes')

    def update_malus_2(self, value):
        self.label_var_2.set(round(value,1))

if __name__ == "__main__":
    app = App()
    app.mainloop()