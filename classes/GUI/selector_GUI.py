import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.schedule = {}

        # configure window
        self.title("Scheduly")
        self.geometry(f"{1340}x{790}")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Run initializing methods
        self.create_sidebar()
        self.create_frames()


    """ Init """
    def create_sidebar(self):

        # Frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Text
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Schedule Selector", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Buttons
        self.student_button = customtkinter.CTkButton(self.sidebar_frame, text="Student", command=self.show_student_frame)
        self.student_button.grid(row=1, column=0, padx=20, pady=20)
        self.course_button = customtkinter.CTkButton(self.sidebar_frame, text="Course", command=self.show_course_frame)
        self.course_button.grid(row=2, column=0, padx=20, pady=20)
        self.room_button = customtkinter.CTkButton(self.sidebar_frame, text="Room", command=self.show_room_frame)
        self.room_button.grid(row=3, column=0, padx=20, pady=20)

        # Export
        self.export_button= customtkinter.CTkButton(self.sidebar_frame, text="Export", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.export)
        self.export_button.grid(row=4, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Export All
        self.export_all_button= customtkinter.CTkButton(self.sidebar_frame, text="Export All", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.export)
        self.export_all_button.grid(row=8, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def create_frames(self):

        # Create student frame
        self.student_frame = customtkinter.CTkFrame(self, width=200, corner_radius=10)
        self.student_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.student_frame.grid_columnconfigure(0, weight=1)
        self.student_frame.grid_rowconfigure((1,2,3,4,5,6), weight=1)

        self.frame_student_content()


        # Create course frame
        self.course_frame = customtkinter.CTkFrame(self, width=200, height=200, corner_radius=10)
        self.course_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.course_frame.grid_columnconfigure(0, weight=1)
        self.course_frame.grid_rowconfigure((1,2,3,4,5,6), weight=1)

        self.frame_course_content()

        # Create room frame
        self.room_frame = customtkinter.CTkFrame(self, width=200, height=200, corner_radius=10)
        self.room_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.room_frame.grid_columnconfigure(0, weight=1)
        self.room_frame.grid_rowconfigure((1,2,3,4,5,6), weight=1)

        self.frame_room_content()

    def frame_student_content(self):

        # Search Frame
        self.student_search_frame = customtkinter.CTkFrame(self.student_frame, corner_radius=10)
        self.student_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.student_search_frame.grid_rowconfigure((0), weight=1)
        self.student_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Student option
        self.student_option = customtkinter.CTkOptionMenu(self.student_search_frame,
                                                values=["Amalia Kro", "Jonas Bollewijk"])
        self.student_option.grid(row=0, column=0, columnspan=7, padx=20, pady=20, sticky="ew")
        self.student_option.set('Student')

        # Student Add Button
        self.student_add_button = customtkinter.CTkButton(self.student_search_frame, text="Search", command=self.student_button_click)
        self.student_add_button.grid(row=0, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Student Roster
        self.student_schedule = customtkinter.CTkFrame(self.student_frame, corner_radius=10)
        self.student_schedule.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="nsew")
        self.student_schedule.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.student_schedule.grid_rowconfigure((0,1,2,3,4), weight=1)

    def frame_course_content(self):

        # Search Frame
        self.course_search_frame = customtkinter.CTkFrame(self.course_frame, corner_radius=10)
        self.course_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.course_search_frame.grid_rowconfigure(0, weight=1)
        self.course_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Course option
        self.course_option = customtkinter.CTkOptionMenu(self.course_search_frame,
                                                values=["Heuristics 2", "Heuristics 1"])
        self.course_option.grid(row=0, column=0, columnspan=7, padx=20, pady=20, sticky="ew")
        self.course_option.set('Course')

        # Course Add Button
        self.course_add_button = customtkinter.CTkButton(self.course_search_frame, text="Search", command=self.course_button_click)
        self.course_add_button.grid(row=0, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Course Roster
        self.course_schedule = customtkinter.CTkFrame(self.course_frame, corner_radius=10)
        self.course_schedule.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="nsew")
        self.course_schedule.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.course_schedule.grid_rowconfigure((0,1,2,3,4), weight=1)

    def frame_room_content(self):

        # Search Frame
        self.room_search_frame = customtkinter.CTkFrame(self.room_frame, corner_radius=10)
        self.room_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.room_search_frame.grid_rowconfigure(0, weight=1)
        self.room_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Room option
        self.room_option = customtkinter.CTkOptionMenu(self.room_search_frame,
                                                values=["C1.102", "C1.103"])
        self.room_option.grid(row=0, column=0, columnspan=7, padx=20, pady=20, sticky="ew")
        self.room_option.set('Room')

        # Room Add Button
        self.room_add_button = customtkinter.CTkButton(self.room_search_frame, text="Search", command=self.room_button_click)
        self.room_add_button.grid(row=0, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Room Roster
        self.room_schedule = customtkinter.CTkFrame(self.room_frame, corner_radius=10)
        self.room_schedule.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="nsew")
        self.room_schedule.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.room_schedule.grid_rowconfigure((0,1,2,3,4), weight=1)

    """ Methods """

    def show_student_frame(self):
        self.student_frame.tkraise()

        # Destroy any prior schedule
        for widget in self.student_schedule.winfo_children():
            widget.destroy()

        self.student_option.set('Student')

    def show_course_frame(self):
        self.course_frame.tkraise()

        # Destroy any prior schedule
        for widget in self.course_schedule.winfo_children():
            widget.destroy()

        self.course_option.set('Course')

    def show_room_frame(self):
        self.room_frame.tkraise()

        # Destroy any prior schedule
        for widget in self.room_schedule.winfo_children():
            widget.destroy()

        self.room_option.set('Room')


    def student_button_click(self):

        student = None
        while student == None:
            student = self.student_option.get()

        frame = self.student_schedule

        self.create_grid(frame)

    def course_button_click(self):

        course = None
        while course == None:
            course = self.course_option.get()

        frame = self.course_schedule

        self.create_grid(frame)

    def room_button_click(self):

        room = None
        while room == None:
            room = self.room_option.get()

        frame = self.room_schedule

        self.create_grid(frame)

    def create_grid(self, frame):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        timeslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]
        timeslot_to_num = {9:0, 11:1, 13:2, 15:3, 17:4}

        for i, day in enumerate(days):
            self.day_label = customtkinter.CTkLabel(master=frame, text=day, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.day_label.grid(row=0, column=i+1, padx=5, pady=10, sticky='nsew')

        for i, timeslot in enumerate(timeslots):
            self.time_label = customtkinter.CTkLabel(master=frame, text=timeslot, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.time_label.grid(row=i+1, column=0, padx=10, pady=5, sticky='nsew')

        for subject, subject_info in self.schedule.items():

            for class_type, class_info in subject_info.items():

                day = class_info['day']
                timeslot = class_info['timeslot']
                room = class_info['room']

                col = timeslot_to_num[timeslot]
                row = days.index(day) + 1

                self._class = customtkinter.CTkLabel(master=frame, text=f"{subject}\n{class_type}\n{room}")
                self._class.grid(row=row, column=col+1, sticky='nsew')

    def export(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()