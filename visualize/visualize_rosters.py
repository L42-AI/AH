import tkinter as tk
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class StudentSchedule(customtkinter.CTk):
    def __init__(self, student_schedule):
        super().__init__()

        # configure window
        self.title("Scheduly")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.student_schedule = student_schedule

        self.create_grid()

    def create_grid(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        timeslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]
        timeslot_to_num = {9:0, 11:1, 13:2, 15:3, 17:4}



        for i, day in enumerate(days):
            tk.Label(self, text=day).grid(row=0, column=i+1)

        for i, timeslot in enumerate(timeslots):
            tk.Label(self, text=timeslot).grid(row=i+1, column=0)

        for subject, subject_info in self.student_schedule.items():
            for class_type, class_info in subject_info.items():
                day = class_info['day']
                timeslot = class_info['timeslot']
                room = class_info['room']
                col = timeslot_to_num[timeslot]
                row = days.index(day) + 1
                tk.Label(self, text=f"{subject} - {class_type} - {room}").grid(row=row, column=col+1)

student_schedule = {
    'Analysemethoden en -technieken': {'lecture 1': {'day': 'Thursday', 'timeslot': 15, 'room': 'A1.04'}}, 'Data Mining': {'lecture 1': {'day': 'Wednesday', 'timeslot': 11, 'room': 'B0.201'}, 'lecture 2': {'day': 'Monday', 'timeslot': 15, 'room': 'A1.04'}, 'tutorial 3': {'day': 'Thursday', 'timeslot': 13, 'room': 'A1.10'}, 'practical 2': {'day': 'Tuesday', 'timeslot': 13, 'room': 'A1.10'}}, 'Lineaire Algebra': {'lecture 1': {'day': 'Friday', 'timeslot': 15, 'room': 'A1.06'}, 'lecture 2': {'day': 'Wednesday', 'timeslot': 11, 'room': 'A1.08'}}, 'Software engineering': {'lecture 1': {'day': 'Wednesday', 'timeslot': 13, 'room': 'C0.110'}, 'tutorial 2': {'day': 'Friday', 'timeslot': 11, 'room': 'C0.110'}, 'practical 1': {'day': 'Wednesday', 'timeslot': 9, 'room': 'A1.10'}}}

if __name__ == "__main__":
    app = StudentSchedule(student_schedule)
    app.mainloop()
