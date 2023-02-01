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

        # Set self objects
        self.schedule = schedule

        # Create converting dict to translate student id to student names
        self.student_convert_dict = self.create_student_convert_dict(student_list)

        # Create shedule dicts
        self.student_schedule_frame_dict, self.course_schedule_frame_dict, self.room_schedule_dict = self.represent_schedule()

        # Configure GUI window
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
        """
        This function creates a dictionary mapping each student id to the stundent name
        """

        student_convert_dict = {}

        # For each student
        for student in student_list:

            # Set student id to string of student first name and last name
            student_convert_dict[student.id] = f'{student.f_name} {student.l_name}'

        return student_convert_dict

    def represent_schedule(self) -> tuple:
        """
        This function takes the schedule as input,
        converts it into schedules for stundets, courses and rooms
        """

        student_schedule_dict = self.init_student_schedule(self.schedule)
        course_schedule_dict = self.init_course_schedule(self.schedule)
        room_schedule_dict = self.init_room_schedule(self.schedule)

        return student_schedule_dict, course_schedule_dict, room_schedule_dict

    def __init_schedule(self, schedule, schedule_type) -> dict:
        """
        This function coverts the input shedule and type into a schedule for each type
        """

        schedule_dict = {}

        # For each course:
        for course in schedule:

            # Skip all 'No course' keys
            if course == "No course":
                continue

            # For each class:
            for _class in schedule[course]:

                # Set this as the class moment
                class_moment = schedule[course][_class]

                # Check schedule type
                if schedule_type == "student":

                    # For each student in this class moment:
                    for student_id in class_moment['students']:

                        # Get the student name from the coverting dictionary
                        student_name = self.get_student_name(student_id)

                        # Make student key if not present in dict
                        if student_name not in schedule_dict:
                            schedule_dict[student_name] = {}

                        # Make course key if not present in student key
                        if course not in schedule_dict[student_name]:
                            schedule_dict[student_name][course] = []

                        # Save all data of interest about this class in tuple
                        class_data = _class, class_moment['day'], class_moment['timeslot'], class_moment['room']

                        # Append the class data to the course key
                        schedule_dict[student_name][course].append(class_data)

                elif schedule_type == "course":

                    # Make course key if not present in dict
                    if course not in schedule_dict:
                        schedule_dict[course] = {}

                    # Save all data of interest about this class in tuple
                    class_data = class_moment['day'], class_moment['timeslot'], class_moment['room']

                    # Set class data to the class key
                    schedule_dict[course][_class] = class_data

                elif schedule_type == "room":

                    # Set room
                    room = class_moment['room']

                    # Make room key if not present in dict
                    if room not in schedule_dict:
                        schedule_dict[room] = []

                    # Save all data of interest about this class in tuple
                    class_data = course, _class, class_moment['day'], class_moment['timeslot']

                    # Append the class data to the course key
                    schedule_dict[room].append(class_data)

        return schedule_dict

    def init_student_schedule(self, schedule) -> dict:
        """
        This function runs the schedule funciton wiht the type "student"
        """
        return self.__init_schedule(schedule, "student")

    def init_course_schedule(self, schedule) -> dict:
        """
        This function runs the schedule funciton wiht the type "course"
        """
        return self.__init_schedule(schedule, "course")

    def init_room_schedule(self, schedule) -> dict:
        """
        This function runs the schedule funciton wiht the type "room"
        """
        return self.__init_schedule(schedule, "room")

    def create_sidebar(self) -> None:
        """
        This function creates the GUI widgets to be displayed in the sidebar
        """

        # Frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.rowconfigure((0,1,2,3,4,5), weight=1)

        # Text
        self.application_name = customtkinter.CTkLabel(self.sidebar_frame, text="Schedule Selector", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.application_name.grid(row=0, column=0, padx=20, pady=20)

        # Buttons
        self.student_button = customtkinter.CTkButton(self.sidebar_frame, text="Student", command=self.show_student_frame)
        self.student_button.grid(row=1, column=0, padx=20, pady=20)
        self.course_button = customtkinter.CTkButton(self.sidebar_frame, text="Course", command=self.show_course_frame)
        self.course_button.grid(row=2, column=0, padx=20, pady=20)
        self.room_button = customtkinter.CTkButton(self.sidebar_frame, text="Room", command=self.show_room_frame)
        self.room_button.grid(row=3, column=0, padx=20, pady=20)

        # Export
        self.export_button = customtkinter.CTkButton(self.sidebar_frame, text="Export", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.export)
        self.export_button.grid(row=4, column=0, padx=20, pady=20, sticky="sew")

        # Export All
        self.export_all_button = customtkinter.CTkButton(self.sidebar_frame, text="Export All", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.export_all)
        self.export_all_button.grid(row=5, column=0, padx=20, pady=20, sticky="sew")

    def create_frames(self) -> None:
        """
        This function creates the GUI frames where the students, courses, or rooms will be shown
        """

        # Create student frame
        self.student_frame = customtkinter.CTkFrame(self, width=200, corner_radius=10)
        self.student_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.student_frame.grid_columnconfigure(0, weight=1)
        self.student_frame.grid_rowconfigure((1,2,3,4,5,6), weight=1)

        # Create the student frame content
        self.student_frame_content()


        # Create course frame
        self.course_frame = customtkinter.CTkFrame(self, width=200, height=200, corner_radius=10)
        self.course_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.course_frame.grid_columnconfigure(0, weight=1)
        self.course_frame.grid_rowconfigure((1,2,3,4,5,6), weight=1)

        # Create the course frame content
        self.course_frame_content()

        # Create room frame
        self.room_frame = customtkinter.CTkFrame(self, width=200, height=200, corner_radius=10)
        self.room_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.room_frame.grid_columnconfigure(0, weight=1)
        self.room_frame.grid_rowconfigure((1,2,3,4,5,6), weight=1)

        # Create the room frame content
        self.room_frame_content()

    def student_frame_content(self) -> None:
        """
        This function creates the GUI widget content for the student frame
        """

        # Search Frame
        self.student_search_frame = customtkinter.CTkFrame(self.student_frame, corner_radius=10)
        self.student_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.student_search_frame.grid_rowconfigure((0), weight=1)
        self.student_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Student option
        self.student_option = customtkinter.CTkOptionMenu(self.student_search_frame,
                                                # Take all students from the student dict and sort the list alphabetically
                                                values=sorted([student for student in self.student_schedule_frame_dict]))
        self.student_option.grid(row=0, column=0, columnspan=7, padx=20, pady=20, sticky="ew")
        self.student_option.set('Student')

        # Student Add Button
        self.student_add_button = customtkinter.CTkButton(self.student_search_frame, text="Search", command=self.student_button_click)
        self.student_add_button.grid(row=0, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Student Schedule Frame
        self.student_schedule_frame = customtkinter.CTkFrame(self.student_frame, corner_radius=10)
        self.student_schedule_frame.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="nsew")
        self.student_schedule_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.student_schedule_frame.grid_rowconfigure((0,1,2,3,4), weight=1)

    def course_frame_content(self) -> None:
        """
        This function creates the GUI widget content for the course frame
        """
        # Search Frame
        self.course_search_frame = customtkinter.CTkFrame(self.course_frame, corner_radius=10)
        self.course_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.course_search_frame.grid_rowconfigure(0, weight=1)
        self.course_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Course option
        self.course_option = customtkinter.CTkOptionMenu(self.course_search_frame,
                                                # Take all courses from the course dict and sort the list alphabetically
                                                values=sorted([course for course in self.course_schedule_frame_dict]))
        self.course_option.grid(row=0, column=0, columnspan=7, padx=20, pady=20, sticky="ew")
        self.course_option.set('Course')

        # Course Add Button
        self.course_add_button = customtkinter.CTkButton(self.course_search_frame, text="Search", command=self.course_button_click)
        self.course_add_button.grid(row=0, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Course Schedule Frame
        self.course_schedule_frame = customtkinter.CTkFrame(self.course_frame, corner_radius=10)
        self.course_schedule_frame.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="nsew")
        self.course_schedule_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.course_schedule_frame.grid_rowconfigure((0,1,2,3,4), weight=1)

    def room_frame_content(self) -> None:
        """
        This function creates the GUI widget content for the room frame
        """

        # Search Frame
        self.room_search_frame = customtkinter.CTkFrame(self.room_frame, corner_radius=10)
        self.room_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.room_search_frame.grid_rowconfigure(0, weight=1)
        self.room_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Room option
        self.room_option = customtkinter.CTkOptionMenu(self.room_search_frame,
                                                values=sorted([room for room in self.room_schedule_dict]))
        self.room_option.grid(row=0, column=0, columnspan=7, padx=20, pady=20, sticky="ew")
        self.room_option.set('Room')

        # Room Add Button
        self.room_add_button = customtkinter.CTkButton(self.room_search_frame, text="Search", command=self.room_button_click)
        self.room_add_button.grid(row=0, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Room Schedule Frame
        self.room_schedule = customtkinter.CTkFrame(self.room_frame, corner_radius=10)
        self.room_schedule.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="nsew")
        self.room_schedule.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.room_schedule.grid_rowconfigure((0,1,2,3,4), weight=1)

    def create_export_directory(self) -> None:
        """
        This function erases the content of / creates the export directories
        """

        # Set the working directory
        working_dir = os.getcwd()

        # Delete content of desired directory if already existent
        if os.path.exists(f'{working_dir}/schedules'):
            shutil.rmtree(f'{working_dir}/schedules')
            os.makedirs(f'{working_dir}/schedules')
        else:
            # Create new directory
            os.makedirs(f'{working_dir}/schedules')

    """ Get """

    def get_student_name(self, id) -> str:
        """
        This function retrieves the student name based on the student id
        """
        return self.student_convert_dict.get(id)

    """ Methods """

    def show_student_frame(self) -> None:
        """
        This function describes what happens when the show student button is clicked
        """

        # Destroy any prior schedule
        for widget in self.student_schedule_frame.winfo_children():
            widget.destroy()

        # Set the seach option to 'Student'
        self.student_option.set('Student')

        # Make the frame visible
        self.student_frame.tkraise()

        # Change shown state
        self.shown = 'student'

    def show_course_frame(self) -> None:
        """
        This function describes what happens when the show course button is clicked
        """

        # Destroy any prior schedule
        for widget in self.course_schedule_frame.winfo_children():
            widget.destroy()

        # Set the seach option to 'Course'
        self.course_option.set('Course')

        # Make the frame visible
        self.course_frame.tkraise()

        # Change shown state
        self.shown = 'course'

    def show_room_frame(self) -> None:
        """
        This function describes what happens when the show room button is clicked
        """
        # Destroy any prior schedule
        for widget in self.room_schedule.winfo_children():
            widget.destroy()

        # Set the seach option to 'Room'
        self.room_option.set('Room')

        # Make the frame visible
        self.room_frame.tkraise()

        # Change shown state
        self.shown = 'room'


    def student_button_click(self) -> None:
        """
        This function describes what happens when the find student button is clicked
        """

        # Get the student from the student option widget
        student = self.student_option.get()

        # Do not run function if no student is selected
        if student == 'Student':
            return

        # Set the frame
        frame = self.student_schedule_frame

        # Run the fill grid function to show schedule
        self.fill_grid(frame, 'student', student)

    def course_button_click(self) -> None:
        """
        This function describes what happens when the find course button is clicked
        """

        # Get the course from the course option widget
        course = self.course_option.get()

        # Do not run function if no course is selected
        if course == 'Course':
            return

        # Set the frame
        frame = self.course_schedule_frame

        # Run the fill grid function to show schedule
        self.fill_grid(frame, 'course', course)

    def room_button_click(self) -> None:
        """
        This function describes what happens when the find room button is clicked
        """

        # Get the course from the room option widget
        room = self.room_option.get()

        # Do not run function if no room is selected
        if room == 'Room':
            return

        # Set the frame
        frame = self.room_schedule

        # Run the fill grid function to show schedule
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
            schedule_dict = self.student_schedule_frame_dict

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
            schedule_dict = self.course_schedule_frame_dict

            # For each class
            for _class in schedule_dict[key]:

                # Unpack class info
                day, timeslot, room = schedule_dict[key][_class]

                # Create widget
                self._class = customtkinter.CTkLabel(master=frame, text=f"{_class}\n{room}")
                self.grid(days, timeslot_to_num, day, timeslot)

        elif search_type == 'room':
            schedule_dict = self.room_schedule_dict

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
            dictionary = self.student_schedule_frame_dict

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
            dictionary = self.course_schedule_frame_dict

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
            dictionary = self.room_schedule_dict

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
        for student in sorted(self.student_schedule_frame_dict):

            # For each course:
            for course in self.student_schedule_frame_dict[student]:

                # For each class:
                for class_data in self.student_schedule_frame_dict[student][course]:

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