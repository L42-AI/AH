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
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        """ Setup Multiprocessing Button """

        # Parallel option
        self.parallel_frame = customtkinter.CTkFrame(self)
        self.parallel_frame.grid(row=2, column=3, padx=20, pady=20, sticky="nsew")
        self.parallel_frame.grid_columnconfigure(0, weight=1)
        self.parallel_frame.grid_rowconfigure(0, weight=1)

        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.parallel_frame, text='Multiprocessing', font=customtkinter.CTkFont(size=15, weight='bold'))
        self.checkbox_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        """ Setup Generate Button """

        # Generate Button
        self.generate_button = customtkinter.CTkButton(master=self, text="Generate", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.generate_button.grid(row=3, column=3, padx=20, pady=20, sticky="nsew")

        """ Optimize Configure Frame """

        self.toggle_frame = customtkinter.CTkFrame(self)
        self.toggle_frame.grid(row=0, column=3, rowspan=2, padx=20, pady=20, sticky="nsew")
        self.toggle_frame.grid_columnconfigure(0, weight=1)
        self.toggle_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        # self.radio_var = tkinter.IntVar(value=0)

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


        """ Malus Configure Frame """

        self.malus_config_frame = customtkinter.CTkFrame(self)
        self.malus_config_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="new")
        self.malus_config_frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)

        self.label_malus = customtkinter.CTkLabel(master=self.malus_config_frame, text="Malus Configuration", font=customtkinter.CTkFont(size=17, weight='bold'))
        self.label_malus.grid(row=0, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

        self.switch_state = 0

        self.malus_switch = customtkinter.CTkCheckBox(master=self.malus_config_frame, text="Configure", font=customtkinter.CTkFont(size=15, weight='bold'), command=lambda: self.malus_slider_state(self.switch_state))
        self.malus_switch.grid(row=0, column=7, pady=20, padx=20, sticky="nsew")

        """ Malus Configure Sliders """

        self.malus_slider_frame = customtkinter.CTkFrame(self)
        self.malus_slider_frame.grid(row=1, column=0, rowspan=3, columnspan=2, padx=20, pady=20, sticky="sew")
        self.malus_slider_frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)


        self.label_slider_1 = customtkinter.CTkLabel(master=self.malus_slider_frame, text="Gap Hours", state="disabled", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_slider_1.grid(row=0, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

        self.slider_1 = customtkinter.CTkSlider(self.malus_slider_frame, from_=0.1, to=3, number_of_steps=15, state="disabled", command=self.update_malus_1)
        self.slider_1.grid(row=1, column=0, columnspan=6, padx=20, pady=20, sticky="sew")

        self.label_var_1 = tkinter.StringVar()

        self.slider_1_number = customtkinter.CTkLabel(master=self.malus_slider_frame, textvariable=self.label_var_1, state="disabled", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.slider_1_number.grid(row=1, column=7, padx=20, pady=20, sticky="ew")


        self.label_slider_2 = customtkinter.CTkLabel(master=self.malus_slider_frame, text="Night Classes", state="disabled", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_slider_2.grid(row=2, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

        self.slider_2 = customtkinter.CTkSlider(self.malus_slider_frame, from_=0.1, to=3, number_of_steps=15, state="disabled", command=self.update_malus_2)
        self.slider_2.grid(row=3, column=0, columnspan=6, padx=20, pady=20, sticky="sew")

        self.label_var_2 = tkinter.StringVar()

        self.slider_2_number = customtkinter.CTkLabel(master=self.malus_slider_frame, textvariable=self.label_var_2, state="disabled", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.slider_2_number.grid(row=3, column=7, padx=20, pady=20, sticky="ew")


        # # set default values
        # self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        # self.checkbox_2.configure(state="disabled")
        # self.switch_2.configure(state="disabled")
        # self.checkbox_1.select()
        # self.switch_1.select()
        # self.radio_button_3.configure(state="disabled")
        # self.appearance_mode_optionemenu.set("Dark")
        # self.scaling_optionemenu.set("100%")
        # self.optionmenu_1.set("CTkOptionmenu")
        # self.combobox_1.set("CTkComboBox")
        # self.slider_1.configure(command=self.progressbar_2.set)
        # self.slider_2.configure(command=self.progressbar_3.set)
        # self.progressbar_1.configure(mode="indeterminnate")
        # self.progressbar_1.start()
        # self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        # self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        # self.seg_button_1.set("Value 2")


    def malus_slider_state(self, state):
        """ This functions enables or disables the malus sliders """

        # If the input checkbox is off:
        if state == 0:

            # Alternate the state
            self.switch_state = 1

            for child in self.malus_slider_frame.winfo_children():
                child.configure(state='normal')

        else:
            # Alternate the state
            self.switch_state = 0

            for child in self.malus_slider_frame.winfo_children():
                child.configure(state='disabled')

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