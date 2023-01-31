import tkinter
import tkinter.messagebox
import customtkinter
import time

import os
import shutil
import pandas as pd

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self, student_list, schedule):
        super().__init__()

        self.schedule = schedule

        self.student_convert_dict = self.create_student_convert_dict(student_list)

        self.student_dict, self.course_dict, self.room_dict = self.represent_schedule()

        # configure window
        self.title("Scheduly")
        self.geometry(f"{1340}x{790}")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Run initializing methods
        self.create_sidebar()
        self.create_frames()

        # Create variable to keep track of shown frame
        self.shown = None

        # Create export directory
        self.create_export_directory()


    """ Init """

    def create_student_convert_dict(self, student_list) -> dict:
        student_convert_dict = {}
        for student in student_list:
            student_convert_dict[student.id] = f'{student.f_name} {student.l_name}'
        return student_convert_dict

    def represent_schedule(self) -> tuple:

        student_dict = self.__init_student_schedule(self.schedule)
        course_dict = self.__init_course_schedule(self.schedule)
        room_dict = self.__init_room_schedule(self.schedule)

        return student_dict, course_dict, room_dict

    def __init_student_schedule(self, schedule) -> dict:

        student_dict = {}

        for course in schedule:

            for _class in schedule[course]:

                timeslot = schedule[course][_class]

                for student_id in schedule[course][_class]['students']:

                    student_name = self.get_student_name(student_id)

                    if student_name not in student_dict:
                        student_dict[student_name] = {}
                    if course not in student_dict[student_name]:
                        student_dict[student_name][course] = []

                    class_data = (_class, timeslot['day'], timeslot['timeslot'], timeslot['room'])

                    student_dict[student_name][course].append(class_data)

        return student_dict

    def __init_course_schedule(self, schedule) -> dict:

        course_dict = {}

        for course in schedule:
            if course == "No course":
                continue

            if course not in course_dict:
                course_dict[course] = {}

            for _class in schedule[course]:

                timeslot = schedule[course][_class]

                class_data = (timeslot['day'], timeslot['timeslot'], timeslot['room'])

                course_dict[course][_class] =(class_data)

        return course_dict

    def __init_room_schedule(self, schedule) -> dict:

        room_dict = {}

        for course in schedule:

            for _class in schedule[course]:

                timeslot = schedule[course][_class]

                if timeslot['room'] not in room_dict:
                    room_dict[timeslot['room']] = []

                class_data = (course, _class, timeslot['day'], timeslot['timeslot'])

                room_dict[timeslot['room']].append(class_data)

        return room_dict

    def create_sidebar(self) -> None:

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
        self.export_all_button= customtkinter.CTkButton(self.sidebar_frame, text="Export All", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.export_all)
        self.export_all_button.grid(row=8, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def create_frames(self) -> None:

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


    def frame_student_content(self) -> None:

        # Search Frame
        self.student_search_frame = customtkinter.CTkFrame(self.student_frame, corner_radius=10)
        self.student_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.student_search_frame.grid_rowconfigure((0), weight=1)
        self.student_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Student option
        self.student_option = customtkinter.CTkOptionMenu(self.student_search_frame,
                                                values=sorted([student for student in self.student_dict]))
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

    def frame_course_content(self) -> None:

        # Search Frame
        self.course_search_frame = customtkinter.CTkFrame(self.course_frame, corner_radius=10)
        self.course_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.course_search_frame.grid_rowconfigure(0, weight=1)
        self.course_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Course option
        self.course_option = customtkinter.CTkOptionMenu(self.course_search_frame,
                                                values=sorted([course for course in self.course_dict]))
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

    def frame_room_content(self) -> None:

        # Search Frame
        self.room_search_frame = customtkinter.CTkFrame(self.room_frame, corner_radius=10)
        self.room_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.room_search_frame.grid_rowconfigure(0, weight=1)
        self.room_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Room option
        self.room_option = customtkinter.CTkOptionMenu(self.room_search_frame,
                                                values=sorted([room for room in self.room_dict]))
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

    def create_export_directory(self) -> None:

        working_dir = os.getcwd()

        if os.path.exists(f'{working_dir}/schedules'):
            shutil.rmtree(f'{working_dir}/schedules')
            os.makedirs(f'{working_dir}/schedules')
        else:
            os.makedirs(f'{working_dir}/schedules')

    """ Get """

    def get_student_name(self, id) -> str:
        return self.student_convert_dict.get(id)

    """ Methods """

    def show_student_frame(self) -> None:
        self.student_frame.tkraise()

        # Destroy any prior schedule
        for widget in self.student_schedule.winfo_children():
            widget.destroy()

        self.student_option.set('Student')

        self.shown = 'student'

    def show_course_frame(self) -> None:
        self.course_frame.tkraise()

        # Destroy any prior schedule
        for widget in self.course_schedule.winfo_children():
            widget.destroy()

        self.course_option.set('Course')

        self.shown = 'course'

    def show_room_frame(self) -> None:
        self.room_frame.tkraise()

        # Destroy any prior schedule
        for widget in self.room_schedule.winfo_children():
            widget.destroy()

        self.room_option.set('Room')

        self.shown = 'room'


    def student_button_click(self) -> None:

        student = None
        while student == None:
            student = self.student_option.get()

        frame = self.student_schedule

        self.fill_grid(frame, 'student', student)

    def course_button_click(self) -> None:

        course = None
        while course == None:
            course = self.course_option.get()

        frame = self.course_schedule

        self.fill_grid(frame, 'course', course)

    def room_button_click(self) -> None:

        room = None
        while room == None:
            room = self.room_option.get()

        frame = self.room_schedule

        self.fill_grid(frame, 'room', room)


    def create_grid(self, frame) -> tuple:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        timeslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]
        timeslot_to_num = {9:0, 11:1, 13:2, 15:3, 17:4}

        for i, day in enumerate(days):
            self.day_label = customtkinter.CTkLabel(master=frame, text=day, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.day_label.grid(row=0, column=i+1, padx=5, pady=10, sticky='nsew')

        for i, timeslot in enumerate(timeslots):
            self.time_label = customtkinter.CTkLabel(master=frame, text=timeslot, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.time_label.grid(row=i+1, column=0, padx=10, pady=5, sticky='nsew')

        return days, timeslot_to_num

    def fill_grid(self, frame, search_type, key) -> None:

        if hasattr(self, '_class'):
            self._class.destroy()

        days, timeslot_to_num = self.create_grid(frame)

        if search_type == 'student':
            schedule_dict = self.student_dict

            # For each course:
            for course in schedule_dict[key]:

                # For each class moment:
                for class_moment in schedule_dict[key][course]:

                    # Unpack class info
                    _class, day, timeslot, room = class_moment

                    # Create widget
                    self._class = customtkinter.CTkLabel(master=frame, text=f"{course}\n{_class}\n{room}")
                    self.grid(days, timeslot_to_num, day, timeslot)

        elif search_type == 'course':
            schedule_dict = self.course_dict

            # For each class
            for _class in schedule_dict[key]:

                # Unpack class info
                day, timeslot, room = schedule_dict[key][_class]

                # Create widget
                self._class = customtkinter.CTkLabel(master=frame, text=f"{_class}\n{room}")
                self.grid(days, timeslot_to_num, day, timeslot)

        elif search_type == 'room':
            schedule_dict = self.room_dict

            # for each class moment:
            for class_moments in schedule_dict[key]:

                # Unpack class info
                course, _class, day, timeslot = class_moments

                # Create widget
                self._class = customtkinter.CTkLabel(master=frame, text=f"{course}\n{_class}")
                self.grid(days, timeslot_to_num, day, timeslot)

    def grid(self, days, timeslot_to_num, day, timeslot) -> None:
        row = timeslot_to_num[timeslot]
        col = days.index(day)

        self._class.grid(row=row+1, column=col+1, sticky='nsew')



    def run(self) -> None:
        self.mainloop()

    def export(self) -> None:

        df_course_list = []
        df_class_list = []
        df_day_list = []
        df_time_list = []
        df_room_list = []


        if self.shown == 'student':
            item = self.student_option.get()
            dictionary = self.student_dict

            for course in dictionary[item]:
                for class_info in dictionary[item][course]:
                    df_course_list.append(course)
                    df_class_list.append(class_info[0])
                    df_day_list.append(class_info[1])
                    df_time_list.append(class_info[2])
                    df_room_list.append(class_info[3])

            df = pd.DataFrame({'Course': df_course_list, 'Class': df_class_list,
                               'Day': df_day_list, 'Time': df_time_list,
                               'Room': df_room_list})

            df.to_csv(f'schedules/{item} schedule.csv', index=False)

        elif self.shown == 'course':
            item = self.course_option.get()
            dictionary = self.course_dict

            for _class in dictionary[item]:

                class_info = dictionary[item][_class]

                df_class_list.append(_class)
                df_day_list.append(class_info[0])
                df_time_list.append(class_info[1])
                df_room_list.append(class_info[2])

            df = pd.DataFrame({'Class': df_class_list,
                               'Day': df_day_list, 'Time': df_time_list,
                               'Room': df_room_list})

            df.to_csv(f'schedules/{item} schedule.csv', index=False)

        else:
            item = self.room_option.get()
            dictionary = self.room_dict

            for class_info in dictionary[item]:

                df_course_list.append(class_info[0])
                df_class_list.append(class_info[1])
                df_day_list.append(class_info[2])
                df_time_list.append(class_info[3])

            df = pd.DataFrame({'Course': df_course_list, 'Class': df_class_list,
                'Day': df_day_list, 'Time': df_time_list})

            df.to_csv(f'schedules/{item} schedule.csv', index=False)

    def export_all(self) -> None:

        df_student_list = []
        df_course_list = []
        df_class_list = []
        df_day_list = []
        df_time_list = []
        df_room_list = []

        # For each student:
        for student in sorted(self.student_dict):

            # For each course:
            for course in self.student_dict[student]:

                # For each class:
                for class_data in self.student_dict[student][course]:

                    # Add all relevant information ito lists
                    df_student_list.append(student)
                    df_course_list.append(course)
                    df_class_list.append(class_data[0])
                    df_day_list.append(class_data[1])
                    df_time_list.append(class_data[2])
                    df_room_list.append(class_data[3])

        df = pd.DataFrame({'Student': df_student_list, 'Course': df_course_list, 'Class': df_class_list,
            'Day': df_day_list, 'Time': df_time_list, 'Room': df_room_list})

        df.to_csv('schedules/complete schedule.csv', index=False)

if __name__ == '__main__':
    app = App()
    app.run()