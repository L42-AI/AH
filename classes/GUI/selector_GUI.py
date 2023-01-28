import tkinter
import tkinter.messagebox
import customtkinter
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.represent_schedule()

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

    def __init_student_convert_dict(student_list) -> dict:
        student_convert_dict = {}
        for student in student_list:
            student_convert_dict[student.id] = student.name
        return student_convert_dict


    def __init_student_schedule(self, schedule) -> dict:

        student_id_dict = {}

        for course in schedule:

            for _class in schedule[course]:

                timeslot = schedule[course][_class]

                for student_id in schedule[course][_class]['students']:

                    if student_id not in student_id_dict:
                        student_id_dict[student_id] = {}
                    if course not in student_id_dict[student_id]:
                        student_id_dict[student_id][course] = []

                    class_data = (_class, timeslot['day'], timeslot['timeslot'], timeslot['room'])

                    student_id_dict[student_id][course].append(class_data)

        return student_id_dict

    def __init_course_schedule(self, schedule) -> dict:

        course_dict = {}

        for course in schedule :
            if course == "No course":
                continue

            for _class in schedule[course]:

                timeslot = schedule[course][_class]

                if course not in course_dict:
                    course_dict[course] = {}

                course_dict[course][_class] = []

                class_data = (timeslot['day'], timeslot['timeslot'], timeslot['room'])

                course_dict[course][_class].append(class_data)

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
                                                values=[str(student) for student in self.student_id_dict])
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
                                                values=[course for course in self.course_dict])
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
                                                values=[room for room in self.room_dict])
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
        print(student)
        self.fill_grid(frame, 'student', student)

    def course_button_click(self):

        course = None
        while course == None:
            course = self.course_option.get()

        frame = self.course_schedule

        self.fill_grid(frame, 'course', course)

    def room_button_click(self):

        room = None
        while room == None:
            room = self.room_option.get()

        frame = self.room_schedule

        self.fill_grid(frame, 'room', room)


    def create_grid(self, frame):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        timeslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]
        timeslot_to_num = {9:0, 11:1, 13:2, 15:3, 17:4}

        for i, day in enumerate(days):
            self.day_label = customtkinter.CTkLabel(master=frame, text=day, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.day_label.grid(row=0, column=i+1, padx=10, pady=10)

        for i, timeslot in enumerate(timeslots):
            self.time_label = customtkinter.CTkLabel(master=frame, text=timeslot, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.time_label.grid(row=i+1, column=0, padx=10, pady=10)

        return days, timeslot_to_num

    def fill_grid(self, frame, search_type, key):

        days, timeslot_to_num = self.create_grid(frame)

        if search_type == 'student':
            schedule_dict = self.student_id_dict
        elif search_type == 'course':
            schedule_dict = self.course_dict
        elif search_type == 'room':
            schedule_dict = self.room_dict

        print(schedule_dict.keys())

        for schedule_object in schedule_dict[key]:
            if type(schedule_object) == tuple:
                course, _class, day, timeslot = schedule_object
            else:
                for class_data in schedule_dict[key][schedule_object]:
                    if len(class_data) == 4:
                        course = schedule_object
                        _class, day, timeslot, room = class_data
                    elif len(class_data) == 3:
                        _class = schedule_object
                        day, timeslot, room = class_data

            row = timeslot_to_num[timeslot]
            col = days.index(day)

            if search_type == 'student':
                self._class = customtkinter.CTkLabel(master=frame, text=f"{course}\n{_class}\n{room}")
            elif search_type == 'course':
                self._class = customtkinter.CTkLabel(master=frame, text=f"{_class}\n{room}")
            else:
                self._class = customtkinter.CTkLabel(master=frame, text=f"{course}\n{_class}")

            self._class.grid(row=row+1, column=col+1, sticky='nsew')

    def represent_schedule(self):
        schedule = {'Programmeren in Java 2': {'practical 1': {'day': 'Monday', 'timeslot': 11, 'room': 'A1.10', 'capacity': 56, 'max students': 20.0, 'students': {23257088, 86291592, 12782624, 20618153, 86000192, 44671041, 21964491, 41585485, 73893840, 7386961, 2550487, 63111000, 64053722, 58332004, 55474917, 61443567, 62701040, 86807027, 47477884}}, 'practical 2': {'day': 'Wednesday', 'timeslot': 9, 'room': 'A1.10', 'capacity': 56, 'max students': 20.0, 'students': {10698627, 20830477, 60661905, 51593625, 47982619, 64393888, 93566383, 88263855, 86988337, 58469172, 10702778, 34262212, 37399898, 77960666, 54395877, 17823206, 34900967, 6723948, 7492204, 23983476}}, 'practical 3': {'day': 'Friday', 'timeslot': 9, 'room': 'B0.201', 'capacity': 48, 'max students': 20.0, 'students': {53585410, 37279234, 64600457, 9332762, 91196968, 22826928, 56749879, 80135353, 670011, 23391676, 94955328, 79879876, 9731271, 94467156, 68601184, 22288615, 88597745, 90296821, 92977271}}, 'practical 4': {'day': 'Wednesday', 'timeslot': 9, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {45414528, 54772132, 48503689, 29640619, 63634350, 46701583, 15249775, 2317551, 99272880, 6913074, 94687383, 97019450, 66433883, 39459642, 44391517, 41153310}}, 'practical 5': {'day': 'Friday', 'timeslot': 13, 'room': 'C1.112', 'capacity': 60, 'max students': 20.0, 'students': {85284256, 33776961, 51791169, 3678531, 15902055, 31416266, 63096281, 27582862, 2416751, 27187154, 88519892, 36903574, 96054456, 58040377, 4709948, 4921119}}, 'practical 6': {'day': 'Thursday', 'timeslot': 9, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {23215240, 37744525, 85236626, 70072978, 79167252, 26857113, 13996448, 1048485, 62105897, 28943658, 8464817, 77896638, 73196865, 23658570, 39905995, 70113753, 83415514, 64947290, 38499176, 92778619}}}, 'Calculus 2': {'lecture 1': {'day': 'Monday', 'timeslot': 15, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {44868097, 53585410, 37279234, 65408517, 14816774, 46701583, 27298319, 58253841, 14179347, 5615125, 74182182, 58699305, 6913074, 4546613, 58040377, 14591033, 78443067, 86000192, 31306819, 70939718, 23658570, 16097870, 21029457, 82412626, 75997788, 28957789, 10609762, 56348773, 85335143, 75585647, 62363761, 22168693, 86180471, 80188025, 47477884, 27925117, 83266686, 58592894, 72526473, 12091019, 33760909, 88855695, 61520025, 10149535, 75446434, 40141996, 26260141, 38296757, 55412918, 96054456, 53139134, 9731271, 78735049, 47932106, 23565001, 73302736, 78544592, 24875739, 87900893, 81155296, 4783858, 34173695, 93361408, 77306636, 79167252, 76661016, 6709529, 56872729, 94686490, 79888156, 6939933, 33672995, 62105897, 46570285, 58469172, 73823548, 3678531, 79617364, 45915482, 23628642, 15902055, 6723948, 87602030, 51741554, 55530367, 56544130, 64600457, 48357272, 64228258, 59220392, 38179241, 97135019, 63634350, 10792879, 88752563, 72665524, 27064249, 11593163, 27187154, 19717077, 83415514, 75623387, 14303208, 32705005, 65978354, 86807027}}, 'tutorial 1': {'day': 'Wednesday', 'timeslot': 13, 'room': 'C1.112', 'capacity': 60, 'max students': 40.0, 'students': {72526473, 46701583, 5615125, 76661016, 56872729, 61520025, 6939933, 75446434, 59220392, 38179241, 26260141, 6913074, 88752563, 72665524, 38296757, 27064249, 53139134, 3678531, 31306819, 70939718, 47932106, 11593163, 73302736, 21029457, 45915482, 81155296, 23628642, 10609762, 15902055, 14303208, 87602030, 51741554, 86180471, 47477884, 27925117, 83266686}}, 'tutorial 2': {'day': 'Thursday', 'timeslot': 11, 'room': 'A1.08', 'capacity': 20, 'max students': 40.0, 'students': {93361408, 44868097, 56544130, 65408517, 14816774, 12091019, 88855695, 14179347, 79167252, 55530367, 48357272, 6709529, 10149535, 64228258, 58699305, 97135019, 58469172, 55412918, 96054456, 58040377, 78443067, 73823548, 86000192, 78735049, 23565001, 23658570, 16097870, 27187154, 79617364, 19717077, 24875739, 75997788, 56348773, 85335143, 32705005, 4783858, 86807027, 58592894, 34173695}}, 'tutorial 3': {'day': 'Friday', 'timeslot': 13, 'room': 'A1.10', 'capacity': 56, 'max students': 40.0, 'students': {53585410, 37279234, 64600457, 77306636, 33760909, 27298319, 58253841, 94686490, 79888156, 33672995, 74182182, 62105897, 40141996, 46570285, 63634350, 10792879, 4546613, 14591033, 9731271, 78544592, 82412626, 83415514, 75623387, 87900893, 28957789, 6723948, 75585647, 62363761, 65978354, 22168693, 80188025}}}, 'Kansrekenen 2': {'lecture 1': {'day': 'Friday', 'timeslot': 15, 'room': 'C1.112', 'capacity': 60, 'max students': 1000, 'students': {79858178, 64296965, 42115591, 18266644, 5615125, 20883994, 58522654, 74182182, 91196968, 91139627, 14671406, 39919665, 84524083, 14591033, 97019450, 89338938, 44940353, 54569540, 78136904, 94467156, 28957789, 61518436, 8522855, 7492204, 59075181, 38329455, 39659121, 51186803, 77240949, 47605891, 97371272, 77636749, 36903574, 20331158, 3685034, 14398123, 99272880, 96054456, 34262212, 9731271, 78735049, 51542218, 22731474, 54310617, 24875739, 55474917, 20239127, 34243356, 72547110, 63955238, 11915563, 81218347, 46570285, 37498675, 58469172, 84110134, 56749879, 49631542, 31633723, 94955328, 56988998, 41585485, 69086548, 58332004, 38499176, 65003379, 5368702, 82688900, 76924297, 63408522, 23798155, 39230359, 63634350, 10792879, 23391676, 79366078, 47462856, 31247305, 41527759, 27187154, 17823206, 32705005, 59544049, 10872825}}, 'lecture 2': {'day': 'Thursday', 'timeslot': 17, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {79858178, 64296965, 42115591, 18266644, 5615125, 20883994, 58522654, 74182182, 91196968, 91139627, 14671406, 39919665, 84524083, 14591033, 97019450, 89338938, 44940353, 54569540, 78136904, 94467156, 28957789, 61518436, 8522855, 7492204, 59075181, 38329455, 39659121, 51186803, 77240949, 47605891, 97371272, 77636749, 36903574, 20331158, 3685034, 14398123, 99272880, 96054456, 34262212, 9731271, 78735049, 51542218, 22731474, 54310617, 24875739, 55474917, 20239127, 34243356, 72547110, 63955238, 11915563, 81218347, 46570285, 37498675, 58469172, 84110134, 56749879, 49631542, 31633723, 94955328, 56988998, 41585485, 69086548, 58332004, 38499176, 65003379, 5368702, 82688900, 76924297, 63408522, 23798155, 39230359, 63634350, 10792879, 23391676, 79366078, 47462856, 31247305, 41527759, 27187154, 17823206, 32705005, 59544049, 10872825}}}, 'Software engineering': {'lecture 1': {'day': 'Monday', 'timeslot': 13, 'room': 'A1.10', 'capacity': 56, 'max students': 1000, 'students': {44868097, 80709893, 65408517, 42115591, 22871048, 14309255, 54026378, 11068043, 65318664, 37744525, 27582862, 21095566, 52552718, 89180944, 48357272, 51593625, 13718298, 9287708, 58565406, 41153310, 58074656, 52715680, 96554914, 1048485, 78243495, 62105897, 11915563, 61060652, 26260141, 14671406, 29640619, 89985072, 25106480, 48601268, 4546613, 99283252, 84110134, 52311353, 89338938, 31633723, 70015932, 78443067, 44671041, 43460038, 60312776, 31247305, 77376714, 3727435, 50143947, 95631564, 41527759, 73302736, 4568018, 27950803, 82872148, 94467156, 88176729, 31103066, 45915482, 33877725, 37830626, 3233378, 40343779, 28357474, 55474917, 22323043, 68409833, 62356458, 5976174, 83210352, 59544049, 4783858, 75599734, 14072826, 73236988}}, 'tutorial 1': {'day': 'Tuesday', 'timeslot': 15, 'room': 'A1.10', 'capacity': 56, 'max students': 40.0, 'students': {44868097, 65408517, 42115591, 22871048, 65318664, 54026378, 11068043, 37744525, 52552718, 89180944, 13718298, 9287708, 58565406, 96554914, 11915563, 61060652, 26260141, 48601268, 4546613, 99283252, 84110134, 52311353, 78443067, 70015932, 31247305, 50143947, 95631564, 73302736, 4568018, 94467156, 88176729, 45915482, 33877725, 37830626, 3233378, 40343779, 68409833, 62356458, 5976174, 73236988}}, 'tutorial 2': {'day': 'Friday', 'timeslot': 9, 'room': 'C1.112', 'capacity': 60, 'max students': 40.0, 'students': {80709893, 14309255, 27582862, 21095566, 48357272, 51593625, 41153310, 58074656, 52715680, 1048485, 78243495, 62105897, 29640619, 14671406, 89985072, 25106480, 89338938, 31633723, 44671041, 43460038, 60312776, 77376714, 3727435, 41527759, 27950803, 82872148, 31103066, 28357474, 22323043, 55474917, 83210352, 59544049, 4783858, 75599734, 14072826}}, 'practical 1': {'day': 'Friday', 'timeslot': 11, 'room': 'B0.201', 'capacity': 48, 'max students': 40.0, 'students': {42115591, 22871048, 14309255, 54026378, 37744525, 27582862, 52552718, 89180944, 48357272, 51593625, 13718298, 9287708, 1048485, 62105897, 61060652, 26260141, 89985072, 48601268, 84110134, 52311353, 89338938, 31633723, 70015932, 43460038, 77376714, 3727435, 50143947, 95631564, 73302736, 4568018, 82872148, 94467156, 31103066, 33877725, 28357474, 55474917, 62356458, 5976174, 83210352, 59544049}}, 'practical 2': {'day': 'Thursday', 'timeslot': 13, 'room': 'B0.201', 'capacity': 48, 'max students': 40.0, 'students': {44868097, 80709893, 65408517, 65318664, 11068043, 21095566, 58565406, 41153310, 58074656, 52715680, 96554914, 78243495, 11915563, 29640619, 14671406, 25106480, 99283252, 4546613, 78443067, 44671041, 60312776, 31247305, 41527759, 27950803, 88176729, 45915482, 37830626, 3233378, 40343779, 22323043, 68409833, 4783858, 75599734, 14072826, 73236988}}}, 'Databases 2': {'lecture 1': {'day': 'Wednesday', 'timeslot': 11, 'room': 'A1.10', 'capacity': 56, 'max students': 1000, 'students': {23257088, 51566595, 11996292, 64296965, 27123462, 59397895, 14816774, 60352393, 5085194, 12091019, 29526540, 52552718, 15187217, 70072978, 90474003, 37701751, 56872729, 82689818, 94686490, 62736669, 78821918, 4921119, 5526560, 3168419, 26207525, 29640619, 40141996, 5517869, 24277163, 86988337, 88752563, 34872117, 49631542, 56749879, 4529208, 96054456, 39459642, 670011, 73823548, 72796858, 77896638, 43902015, 46989508, 54540997, 26406342, 47932106, 51542218, 43027916, 72456780, 23658570, 75005528, 77960666, 64947290, 76123484, 57467488, 58083680, 58332004, 42196732, 17222374, 13092455, 83869542, 56191333, 25077484, 17092717, 247918, 91527663, 40434933, 56121590, 86180471, 47477884, 13132925, 58592894}}, 'tutorial 1': {'day': 'Friday', 'timeslot': 15, 'room': 'A1.08', 'capacity': 20, 'max students': 40.0, 'students': {23257088, 51566595, 11996292, 64296965, 27123462, 59397895, 14816774, 60352393, 5085194, 12091019, 29526540, 15187217, 70072978, 90474003, 37701751, 56872729, 82689818, 62736669, 3168419, 40141996, 86988337, 88752563, 56749879, 72796858, 77896638, 46989508, 54540997, 43027916, 72456780, 75005528, 64947290, 57467488, 58332004, 56191333, 17222374, 91527663, 40434933, 86180471, 42196732, 13132925}}, 'tutorial 2': {'day': 'Thursday', 'timeslot': 11, 'room': 'A1.10', 'capacity': 56, 'max students': 40.0, 'students': {52552718, 94686490, 78821918, 4921119, 5526560, 26207525, 29640619, 24277163, 5517869, 34872117, 49631542, 96054456, 4529208, 39459642, 670011, 73823548, 43902015, 26406342, 47932106, 51542218, 23658570, 77960666, 76123484, 58083680, 83869542, 13092455, 25077484, 17092717, 247918, 56121590, 47477884, 58592894}}}, 'Compilerbouw': {'lecture 1': {'day': 'Tuesday', 'timeslot': 15, 'room': 'B0.201', 'capacity': 48, 'max students': 1000, 'students': {37770881, 92665222, 14309255, 86291592, 48503689, 88855695, 13284244, 79167252, 94687383, 76661016, 66701209, 2079771, 75664412, 49683101, 58522654, 34243356, 1766560, 9067939, 54772132, 11741347, 11915563, 81385263, 10792879, 86988337, 8464817, 84524083, 5595824, 34872117, 88752563, 15911353, 80135353, 39459642, 31194811, 72796858, 77896638, 34110913, 3407554, 46989508, 65852230, 60312776, 42778953, 76802764, 95631564, 43689934, 68315599, 40791377, 27187154, 7957843, 27950803, 53202517, 79033175, 13911001, 72895450, 83266686, 88636924, 44391517, 98105190, 12077419, 6723948, 48308205, 65960683, 2317551, 30658799, 95007221, 75599734, 24613625, 73236988, 5368702, 75759231}}, 'lecture 2': {'day': 'Friday', 'timeslot': 9, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {37770881, 92665222, 14309255, 86291592, 48503689, 88855695, 13284244, 79167252, 94687383, 76661016, 66701209, 2079771, 75664412, 49683101, 58522654, 34243356, 1766560, 9067939, 54772132, 11741347, 11915563, 81385263, 10792879, 86988337, 8464817, 84524083, 5595824, 34872117, 88752563, 15911353, 80135353, 39459642, 31194811, 72796858, 77896638, 34110913, 3407554, 46989508, 65852230, 60312776, 42778953, 76802764, 95631564, 43689934, 68315599, 40791377, 27187154, 7957843, 27950803, 53202517, 79033175, 13911001, 72895450, 83266686, 88636924, 44391517, 98105190, 12077419, 6723948, 48308205, 65960683, 2317551, 30658799, 95007221, 75599734, 24613625, 73236988, 5368702, 75759231}}, 'tutorial 1': {'day': 'Wednesday', 'timeslot': 15, 'room': 'B0.201', 'capacity': 48, 'max students': 40.0, 'students': {92665222, 14309255, 86291592, 88855695, 13284244, 2079771, 75664412, 34243356, 1766560, 9067939, 54772132, 11741347, 11915563, 81385263, 10792879, 86988337, 8464817, 84524083, 34872117, 80135353, 39459642, 31194811, 77896638, 34110913, 65852230, 60312776, 95631564, 43689934, 40791377, 53202517, 13911001, 65960683, 2317551, 30658799, 24613625, 5368702, 75759231}}, 'tutorial 2': {'day': 'Monday', 'timeslot': 15, 'room': 'C1.112', 'capacity': 60, 'max students': 40.0, 'students': {37770881, 48503689, 79167252, 94687383, 76661016, 66701209, 49683101, 58522654, 5595824, 88752563, 15911353, 72796858, 3407554, 46989508, 42778953, 76802764, 68315599, 27187154, 7957843, 27950803, 79033175, 72895450, 88636924, 44391517, 98105190, 12077419, 6723948, 48308205, 95007221, 75599734, 73236988, 83266686}}, 'practical 1': {'day': 'Friday', 'timeslot': 15, 'room': 'B0.201', 'capacity': 48, 'max students': 40.0, 'students': {37770881, 92665222, 14309255, 86291592, 48503689, 88855695, 13284244, 79167252, 49683101, 1766560, 81385263, 8464817, 84524083, 15911353, 31194811, 34110913, 3407554, 46989508, 60312776, 42778953, 95631564, 43689934, 68315599, 7957843, 27950803, 79033175, 13911001, 72895450, 83266686, 98105190, 65960683, 48308205, 2317551, 30658799, 95007221, 75599734, 88636924, 5368702, 75759231}}, 'practical 2': {'day': 'Friday', 'timeslot': 11, 'room': 'C1.112', 'capacity': 60, 'max students': 40.0, 'students': {94687383, 76661016, 66701209, 2079771, 75664412, 34243356, 58522654, 9067939, 54772132, 11741347, 11915563, 10792879, 5595824, 86988337, 88752563, 34872117, 80135353, 39459642, 72796858, 77896638, 65852230, 76802764, 40791377, 27187154, 53202517, 44391517, 12077419, 6723948, 24613625, 73236988}}}, 'Netwerken en systeembeveiliging': {'practical 1': {'day': 'Friday', 'timeslot': 11, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {85284256, 16912993, 7308727, 26207525, 33930505, 535689, 25557516, 64246605, 81385263, 12170832, 3883025, 72665524, 77392404, 87830198, 59887191, 44901052, 30195935}}, 'practical 2': {'day': 'Friday', 'timeslot': 15, 'room': 'A1.04', 'capacity': 41, 'max students': 20.0, 'students': {57467488, 28618400, 53267490, 54772132, 56191333, 70939718, 8522855, 38499176, 86291592, 63573738, 19058315, 37744525, 62363761, 72586808, 4353500}}, 'practical 3': {'day': 'Friday', 'timeslot': 13, 'room': 'A1.04', 'capacity': 41, 'max students': 20.0, 'students': {40343779, 31247305, 60352393, 14398123, 70844780, 59075181, 66120270, 29640619, 72456780, 48678993, 1696500, 81200278, 82689818, 123355, 75664412, 62736669}}, 'practical 4': {'day': 'Thursday', 'timeslot': 13, 'room': 'C1.112', 'capacity': 60, 'max students': 20.0, 'students': {1048485, 34243356, 97136582, 9731271, 97135019, 21677389, 25330192, 5590289, 51741554, 7957843, 82872148, 18266644, 36903574, 56121590, 81022997, 4709948}}}, 'Collectieve Intelligentie': {'lecture 1': {'day': 'Monday', 'timeslot': 13, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {37770881, 64296965, 86291592, 72577292, 33760909, 82689818, 9332762, 58522654, 42171678, 64393888, 64228258, 46052388, 13534377, 22699561, 97135019, 29640619, 5517869, 35330349, 24277163, 17575088, 29474737, 25106480, 48601268, 7308727, 34773179, 1665980, 77896638, 1075391, 86000192, 26406342, 60312776, 42778953, 31416266, 50143947, 21964491, 43027916, 73980360, 54310617, 76123484, 68601184, 3233378, 23547619, 28357474, 53107172, 17222374, 87758823, 15902055, 13092455, 96104167, 65960683, 75521763, 61443567, 62701040, 45556081, 51741554, 4783858, 1696500, 77240949, 57595888, 42196732, 50184318}}, 'lecture 2': {'day': 'Thursday', 'timeslot': 11, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {37770881, 64296965, 86291592, 72577292, 33760909, 82689818, 9332762, 58522654, 42171678, 64393888, 64228258, 46052388, 13534377, 22699561, 97135019, 29640619, 5517869, 35330349, 24277163, 17575088, 29474737, 25106480, 48601268, 7308727, 34773179, 1665980, 77896638, 1075391, 86000192, 26406342, 60312776, 42778953, 31416266, 50143947, 21964491, 43027916, 73980360, 54310617, 76123484, 68601184, 3233378, 23547619, 28357474, 53107172, 17222374, 87758823, 15902055, 13092455, 96104167, 65960683, 75521763, 61443567, 62701040, 45556081, 51741554, 4783858, 1696500, 77240949, 57595888, 42196732, 50184318}}, 'lecture 3': {'day': 'Tuesday', 'timeslot': 13, 'room': 'B0.201', 'capacity': 48, 'max students': 1000, 'students': {37770881, 64296965, 86291592, 72577292, 33760909, 82689818, 9332762, 58522654, 42171678, 64393888, 64228258, 46052388, 13534377, 22699561, 97135019, 29640619, 5517869, 35330349, 24277163, 17575088, 29474737, 25106480, 48601268, 7308727, 34773179, 1665980, 77896638, 1075391, 86000192, 26406342, 60312776, 42778953, 31416266, 50143947, 21964491, 43027916, 73980360, 54310617, 76123484, 68601184, 3233378, 23547619, 28357474, 53107172, 17222374, 87758823, 15902055, 13092455, 96104167, 65960683, 75521763, 61443567, 62701040, 45556081, 51741554, 4783858, 1696500, 77240949, 57595888, 42196732, 50184318}}, 'tutorial 1': {'day': 'Thursday', 'timeslot': 15, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {72577292, 33760909, 9332762, 42171678, 64228258, 46052388, 22699561, 97135019, 17575088, 7308727, 1665980, 1075391, 50143947, 43027916, 3233378, 17222374, 13092455, 51741554, 77240949, 50184318}}, 'tutorial 2': {'day': 'Tuesday', 'timeslot': 9, 'room': 'A1.04', 'capacity': 41, 'max students': 20.0, 'students': {28357474, 75521763, 64296965, 86291592, 42778953, 13534377, 31416266, 60312776, 35330349, 73980360, 62701040, 57595888, 4783858, 48601268, 54310617, 34773179}}, 'tutorial 3': {'day': 'Wednesday', 'timeslot': 15, 'room': 'C1.112', 'capacity': 60, 'max students': 20.0, 'students': {64393888, 96104167, 87758823, 29640619, 5517869, 45556081, 29474737, 77896638}}, 'tutorial 4': {'day': 'Monday', 'timeslot': 13, 'room': 'C1.112', 'capacity': 60, 'max students': 20.0, 'students': {86000192, 68601184, 37770881, 23547619, 42196732, 53107172, 26406342, 15902055, 21964491, 65960683, 24277163, 61443567, 25106480, 1696500, 82689818, 76123484, 58522654}}, 'practical 1': {'day': 'Thursday', 'timeslot': 15, 'room': 'C1.112', 'capacity': 60, 'max students': 20.0, 'students': {9332762, 42171678, 58522654, 46052388, 97135019, 35330349, 25106480, 34773179, 1075391, 86000192, 42778953, 31416266, 50143947, 3233378, 23547619, 87758823, 15902055, 13092455, 4783858, 1696500}}, 'practical 2': {'day': 'Wednesday', 'timeslot': 11, 'room': 'A1.04', 'capacity': 41, 'max students': 20.0, 'students': {75521763, 64296965, 60312776, 22699561, 43027916, 33760909, 61443567, 62701040, 17575088, 51741554, 57595888, 76123484, 1665980}}, 'practical 3': {'day': 'Tuesday', 'timeslot': 13, 'room': 'C1.112', 'capacity': 60, 'max students': 20.0, 'students': {37770881, 21964491, 65960683, 5517869, 24277163, 45556081, 29474737, 77896638, 7308727, 82689818, 42196732, 50184318}}, 'practical 4': {'day': 'Monday', 'timeslot': 15, 'room': 'A1.10', 'capacity': 56, 'max students': 20.0, 'students': {64393888, 68601184, 64228258, 28357474, 53107172, 17222374, 96104167, 86291592, 13534377, 26406342, 29640619, 72577292, 73980360, 48601268, 77240949, 54310617}}}, 'Lineaire Algebra': {'lecture 1': {'day': 'Tuesday', 'timeslot': 13, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {62872965, 80709893, 42115591, 32595335, 16333449, 56872729, 34588570, 36508571, 16011419, 94686490, 34243356, 10149535, 4921119, 74182182, 91196968, 81218347, 61060652, 5517869, 35330349, 81385263, 93566383, 79937969, 71839156, 3474870, 55412918, 54074680, 52311353, 14591033, 670011, 77896638, 94955328, 42778953, 31416266, 23565001, 16097870, 90743504, 66570705, 96118484, 79617364, 58866007, 75005528, 37399898, 21311067, 36527838, 26172512, 55474917, 87758823, 38499176, 68409833, 48308205, 83210352, 80998260, 41578612, 42196732}}, 'lecture 2': {'day': 'Thursday', 'timeslot': 9, 'room': 'C1.112', 'capacity': 60, 'max students': 1000, 'students': {62872965, 80709893, 42115591, 32595335, 16333449, 56872729, 34588570, 36508571, 16011419, 94686490, 34243356, 10149535, 4921119, 74182182, 91196968, 81218347, 61060652, 5517869, 35330349, 81385263, 93566383, 79937969, 71839156, 3474870, 55412918, 54074680, 52311353, 14591033, 670011, 77896638, 94955328, 42778953, 31416266, 23565001, 16097870, 90743504, 66570705, 96118484, 79617364, 58866007, 75005528, 37399898, 21311067, 36527838, 26172512, 55474917, 87758823, 38499176, 68409833, 48308205, 83210352, 80998260, 41578612, 42196732}}}, 'Moderne Databases': {'lecture 1': {'day': 'Thursday', 'timeslot': 13, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {11996292, 14309255, 64600457, 29526540, 43680781, 48198668, 89180944, 13218321, 36748818, 3883025, 70072978, 27241113, 42171678, 78821918, 1766560, 11741347, 78243495, 58699305, 18144425, 15051051, 24277163, 5517869, 46570285, 99283252, 49631542, 51650744, 78443067, 4709948, 33776961, 59111489, 27916487, 47462856, 77376714, 68315599, 78544592, 63111000, 13911001, 83415514, 49219163, 75997788, 83266686, 36527838, 75521763, 58332004, 17222374, 85335143, 58592894, 96082155, 41489515, 84449005, 66621166, 30658799, 1181560, 50184318}}, 'tutorial 1': {'day': 'Friday', 'timeslot': 13, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {14309255, 43680781, 13218321, 36748818, 70072978, 1766560, 78243495, 18144425, 33776961, 59111489, 27916487, 47462856, 68315599, 63111000, 49219163, 75997788, 36527838, 58332004, 84449005, 58592894}}, 'tutorial 2': {'day': 'Monday', 'timeslot': 15, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {11996292, 29526540, 89180944, 3883025, 27241113, 42171678, 15051051, 46570285, 99283252, 51650744, 77376714, 78544592, 13911001, 83415514, 75521763, 66621166, 30658799, 50184318, 83266686}}, 'tutorial 3': {'day': 'Monday', 'timeslot': 11, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {11741347, 17222374, 85335143, 58699305, 64600457, 96082155, 41489515, 5517869, 48198668, 24277163, 49631542, 1181560, 78443067, 4709948, 78821918}}, 'practical 1': {'day': 'Wednesday', 'timeslot': 9, 'room': 'B0.201', 'capacity': 48, 'max students': 20.0, 'students': {14309255, 29526540, 89180944, 78821918, 42171678, 78243495, 24277163, 46570285, 49631542, 33776961, 77376714, 68315599, 78544592, 63111000, 58332004, 17222374, 96082155, 84449005, 66621166, 58592894}}, 'practical 2': {'day': 'Wednesday', 'timeslot': 15, 'room': 'A1.10', 'capacity': 56, 'max students': 20.0, 'students': {43680781, 13218321, 36748818, 27241113, 18144425, 15051051, 5517869, 99283252, 51650744, 59111489, 27916487, 47462856, 13911001, 83415514, 49219163, 36527838, 85335143, 41489515, 1181560, 50184318}}, 'practical 3': {'day': 'Tuesday', 'timeslot': 15, 'room': 'A1.04', 'capacity': 41, 'max students': 20.0, 'students': {1766560, 11741347, 11996292, 75521763, 58699305, 64600457, 48198668, 30658799, 3883025, 70072978, 83266686, 78443067, 75997788, 4709948}}}, 'Reflectie op de digitale cultuur': {'lecture 1': {'day': 'Wednesday', 'timeslot': 11, 'room': 'B0.201', 'capacity': 48, 'max students': 1000, 'students': {36785409, 37110913, 22871048, 60352393, 43680781, 60661905, 90474003, 77392404, 68286356, 20239127, 13718298, 82390428, 36213792, 52715680, 96554914, 49922855, 3685034, 24277163, 22826928, 86988337, 99975346, 84524083, 6913074, 38296757, 87830198, 5298748, 4709948, 51415617, 33776961, 13658563, 54569540, 51052738, 42406214, 78136904, 99453514, 57086672, 27950803, 77960666, 37399898, 32044893, 27805666, 27370083, 61518436, 59753700, 13092455, 70193386, 70844780, 84449005, 41578612, 20095994, 92778619}}, 'lecture 2': {'day': 'Friday', 'timeslot': 11, 'room': 'A1.04', 'capacity': 41, 'max students': 1000, 'students': {36785409, 37110913, 22871048, 60352393, 43680781, 60661905, 90474003, 77392404, 68286356, 20239127, 13718298, 82390428, 36213792, 52715680, 96554914, 49922855, 3685034, 24277163, 22826928, 86988337, 99975346, 84524083, 6913074, 38296757, 87830198, 5298748, 4709948, 51415617, 33776961, 13658563, 54569540, 51052738, 42406214, 78136904, 99453514, 57086672, 27950803, 77960666, 37399898, 32044893, 27805666, 27370083, 61518436, 59753700, 13092455, 70193386, 70844780, 84449005, 41578612, 20095994, 92778619}}, 'tutorial 1': {'day': 'Wednesday', 'timeslot': 9, 'room': 'C1.112', 'capacity': 60, 'max students': 20.0, 'students': {52715680, 51415617, 96554914, 37110913, 54569540, 22871048, 3685034, 70193386, 70844780, 84449005, 77392404, 68286356, 13718298, 92778619}}, 'tutorial 2': {'day': 'Friday', 'timeslot': 11, 'room': 'A1.10', 'capacity': 56, 'max students': 20.0, 'students': {60352393, 90474003, 20239127, 36213792, 49922855, 24277163, 22826928, 99975346, 84524083, 38296757, 5298748, 51052738, 42406214, 99453514, 27950803, 37399898, 27805666, 27370083, 61518436, 59753700}}, 'tutorial 3': {'day': 'Tuesday', 'timeslot': 9, 'room': 'A1.10', 'capacity': 56, 'max students': 20.0, 'students': {36785409, 33776961, 13658563, 13092455, 78136904, 43680781, 57086672, 60661905, 86988337, 77960666, 6913074, 41578612, 87830198, 82390428, 20095994, 4709948, 32044893}}}, 'Analysemethoden en -technieken': {'lecture 1': {'day': 'Friday', 'timeslot': 15, 'room': 'A1.10', 'capacity': 56, 'max students': 1000, 'students': {36785409, 56544130, 73350019, 64296965, 42115591, 22871048, 65318664, 5085194, 23798155, 60661905, 18266644, 48357272, 13718298, 34243356, 78821918, 4921119, 58480929, 82854435, 33672995, 5595824, 62613937, 56815156, 87830198, 72586808, 52311353, 97019450, 14637758, 94955328, 83443653, 23565001, 51542218, 23658570, 43027916, 72456780, 16097870, 73302736, 57086672, 48678993, 75997788, 97838175, 18477924, 88737765, 78822885, 85335143, 34900967, 77831658, 70193386, 41578612, 80188025}}}, 'Bioinformatica': {'lecture 1': {'day': 'Thursday', 'timeslot': 9, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {44868097, 14816774, 33930505, 54026378, 11068043, 29526540, 43680781, 64600457, 28359697, 81200278, 20883994, 58522654, 3168419, 15051051, 22826928, 89985072, 6913074, 56815156, 56749879, 96054456, 7308727, 14591033, 5298748, 21964491, 66120270, 21029457, 22731474, 4568018, 74131924, 53202517, 79617364, 88176729, 33877725, 30195935, 42196732, 85335143, 70878567, 77831658, 6723948, 247918, 59544049, 96453361, 30050930, 24613625, 73236988}}, 'lecture 2': {'day': 'Tuesday', 'timeslot': 17, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {44868097, 14816774, 33930505, 54026378, 11068043, 29526540, 43680781, 64600457, 28359697, 81200278, 20883994, 58522654, 3168419, 15051051, 22826928, 89985072, 6913074, 56815156, 56749879, 96054456, 7308727, 14591033, 5298748, 21964491, 66120270, 21029457, 22731474, 4568018, 74131924, 53202517, 79617364, 88176729, 33877725, 30195935, 42196732, 85335143, 70878567, 77831658, 6723948, 247918, 59544049, 96453361, 30050930, 24613625, 73236988}}, 'lecture 3': {'day': 'Monday', 'timeslot': 15, 'room': 'A1.04', 'capacity': 41, 'max students': 1000, 'students': {44868097, 14816774, 33930505, 54026378, 11068043, 29526540, 43680781, 64600457, 28359697, 81200278, 20883994, 58522654, 3168419, 15051051, 22826928, 89985072, 6913074, 56815156, 56749879, 96054456, 7308727, 14591033, 5298748, 21964491, 66120270, 21029457, 22731474, 4568018, 74131924, 53202517, 79617364, 88176729, 33877725, 30195935, 42196732, 85335143, 70878567, 77831658, 6723948, 247918, 59544049, 96453361, 30050930, 24613625, 73236988}}, 'tutorial 1': {'day': 'Wednesday', 'timeslot': 13, 'room': 'B0.201', 'capacity': 48, 'max students': 20.0, 'students': {88176729, 85335143, 54026378, 21964491, 29526540, 247918, 66120270, 22826928, 59544049, 28359697, 89985072, 74131924, 56815156, 53202517, 24613625, 58522654, 14591033}}, 'tutorial 2': {'day': 'Monday', 'timeslot': 11, 'room': 'A1.04', 'capacity': 41, 'max students': 20.0, 'students': {42196732, 14816774, 73236988, 21029457, 4568018, 6913074, 96453361, 30050930, 81200278, 56749879, 96054456, 5298748, 33877725, 30195935}}, 'tutorial 3': {'day': 'Thursday', 'timeslot': 11, 'room': 'C1.112', 'capacity': 60, 'max students': 20.0, 'students': {44868097, 3168419, 70878567, 33930505, 77831658, 11068043, 64600457, 43680781, 6723948, 15051051, 22731474, 79617364, 7308727, 20883994}}, 'practical 1': {'day': 'Monday', 'timeslot': 13, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {14816774, 70878567, 54026378, 15051051, 29526540, 66120270, 22826928, 89985072, 4568018, 6913074, 30050930, 7308727, 96054456, 24613625, 20883994, 73236988}}, 'practical 2': {'day': 'Monday', 'timeslot': 11, 'room': 'C1.112', 'capacity': 60, 'max students': 20.0, 'students': {44868097, 3168419, 42196732, 14591033, 33930505, 21964491, 6723948, 247918, 21029457, 96453361, 81200278, 56749879, 88176729, 5298748, 33877725, 30195935}}, 'practical 3': {'day': 'Monday', 'timeslot': 9, 'room': 'A1.04', 'capacity': 41, 'max students': 20.0, 'students': {85335143, 64600457, 77831658, 11068043, 43680781, 59544049, 28359697, 22731474, 74131924, 56815156, 53202517, 79617364, 58522654}}}, 'Heuristieken 1': {'lecture 1': {'day': 'Thursday', 'timeslot': 9, 'room': 'A1.10', 'capacity': 56, 'max students': 1000, 'students': {66122625, 37110913, 11996292, 14816774, 22871048, 20830477, 87210640, 58736785, 36903574, 20331158, 48357272, 14138904, 42171678, 76393508, 53775014, 97417002, 19858730, 61060652, 81218347, 71839156, 56749879, 14941752, 14591033, 97019450, 44901052, 13658563, 79879876, 83443653, 31897288, 4568018, 4353500, 75997788, 57467488, 22323043, 53107172, 75521763, 98105190, 94930277, 59075181, 4783858, 86807027, 1696500, 92977271, 45660925}}, 'tutorial 1': {'day': 'Thursday', 'timeslot': 15, 'room': 'A1.10', 'capacity': 56, 'max students': 25.0, 'students': {66122625, 22871048, 20331158, 76393508, 53775014, 81218347, 61060652, 71839156, 79879876, 31897288, 4568018, 4353500, 75997788, 57467488, 22323043, 75521763, 94930277, 86807027, 45660925}}, 'tutorial 2': {'day': 'Wednesday', 'timeslot': 15, 'room': 'A1.04', 'capacity': 41, 'max students': 25.0, 'students': {37110913, 11996292, 14816774, 20830477, 87210640, 58736785, 36903574, 48357272, 14138904, 42171678, 97417002, 19858730, 56749879, 14941752, 14591033, 97019450, 44901052, 13658563, 83443653, 53107172, 98105190, 59075181, 4783858, 1696500, 92977271}}}, 'Project Numerical Recipes': {'practical 1': {'day': 'Tuesday', 'timeslot': 15, 'room': 'C1.112', 'capacity': 60, 'max students': 15.0, 'students': {28618400, 37419523, 60312776, 42778953, 77831658, 63573738, 3685034, 48503689, 40911986, 22731474, 2550487, 12430748, 89338938, 73823548}}, 'practical 2': {'day': 'Wednesday', 'timeslot': 13, 'room': 'A1.08', 'capacity': 20, 'max students': 15.0, 'students': {13996448, 19214659, 32183908, 74182182, 13092455, 63939720, 42406214, 11068043, 34691309, 86807027, 7308727, 75005528, 72895450, 73236988, 32044893}}, 'practical 3': {'day': 'Thursday', 'timeslot': 9, 'room': 'B0.201', 'capacity': 48, 'max students': 15.0, 'students': {1766560, 81116418, 90103047, 86291592, 62356458, 19662602, 48308205, 7957843, 13284244, 81022997, 84110134, 21070547, 14941752, 88752563, 6939933}}}, 'Algoritmen en complexiteit': {'lecture 1': {'day': 'Friday', 'timeslot': 11, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {19540225, 53585410, 51566595, 44828429, 21095566, 46701583, 27298319, 36903574, 82689818, 52715680, 88596522, 26260141, 14671406, 81385263, 86988337, 67817269, 3474870, 3707829, 1665980, 51509565, 43902015, 23652927, 78136904, 77376714, 50143947, 64554442, 41585485, 21964491, 41527759, 72895450, 66433883, 64947290, 57467488, 40343779, 8522855, 15902055, 12077419, 34765676, 5976174, 91527663, 96453361, 23983476, 58592894}}, 'tutorial 1': {'day': 'Tuesday', 'timeslot': 13, 'room': 'A1.04', 'capacity': 41, 'max students': 25.0, 'students': {53585410, 40343779, 51566595, 88596522, 12077419, 50143947, 41585485, 26260141, 81385263, 34765676, 86988337, 21964491, 96453361, 23983476, 67817269, 3474870, 64947290, 51509565}}, 'tutorial 2': {'day': 'Monday', 'timeslot': 13, 'room': 'B0.201', 'capacity': 48, 'max students': 25.0, 'students': {19540225, 44828429, 21095566, 46701583, 27298319, 36903574, 82689818, 52715680, 14671406, 3707829, 1665980, 43902015, 23652927, 78136904, 77376714, 64554442, 41527759, 72895450, 66433883, 57467488, 8522855, 15902055, 5976174, 91527663, 58592894}}, 'practical 1': {'day': 'Tuesday', 'timeslot': 11, 'room': 'B0.201', 'capacity': 48, 'max students': 25.0, 'students': {19540225, 51566595, 44828429, 21095566, 46701583, 82689818, 26260141, 14671406, 3707829, 3474870, 51509565, 23652927, 78136904, 41585485, 72895450, 64947290, 40343779, 8522855, 15902055, 34765676, 5976174, 91527663, 96453361, 23983476}}, 'practical 2': {'day': 'Tuesday', 'timeslot': 9, 'room': 'B0.201', 'capacity': 48, 'max students': 25.0, 'students': {53585410, 27298319, 36903574, 52715680, 88596522, 81385263, 86988337, 67817269, 1665980, 43902015, 77376714, 50143947, 64554442, 21964491, 41527759, 66433883, 57467488, 12077419, 58592894}}}, 'Zoeken sturen en bewegen': {'practical 1': {'day': 'Tuesday', 'timeslot': 9, 'room': 'C1.112', 'capacity': 60, 'max students': 15.0, 'students': {13116738, 9067939, 13658563, 63955238, 60352393, 15051051, 27298319, 82233873, 58253841, 96453361, 37804282, 42171678, 44391517, 36527838, 57419039}}, 'practical 2': {'day': 'Wednesday', 'timeslot': 9, 'room': 'A1.04', 'capacity': 41, 'max students': 15.0, 'students': {23547619, 13210212, 59753700, 88597745, 28359697, 56815156, 53202517, 59887191, 4529208, 37399898, 28957789, 41644639}}, 'practical 3': {'day': 'Friday', 'timeslot': 13, 'room': 'B0.201', 'capacity': 48, 'max students': 15.0, 'students': {57701414, 87758823, 59220392, 33946407, 97135019, 6723948, 68315599, 24167153, 90474003, 3707829, 88627897, 45915482, 92778619, 76123484, 97838175}}}, 'Compilerbouw practicum': {'practical 1': {'day': 'Monday', 'timeslot': 9, 'room': 'A1.08', 'capacity': 20, 'max students': 15.0, 'students': {11459236, 26406342, 38499176, 535689, 5085194, 89985072, 14383795, 71839156, 42297781, 65675896, 13911001, 1665980, 64418623}}, 'practical 2': {'day': 'Monday', 'timeslot': 11, 'room': 'B0.201', 'capacity': 48, 'max students': 15.0, 'students': {91250534, 47260040, 14303208, 88596522, 50143947, 63634350, 44151631, 99272880, 57595888, 4568018, 51673172, 82066165, 74361881, 41644639}}, 'practical 3': {'day': 'Thursday', 'timeslot': 13, 'room': 'A1.10', 'capacity': 56, 'max students': 15.0, 'students': {25994016, 55103073, 53585410, 3407554, 52715680, 23215240, 51472074, 11068043, 32204977, 72665524, 14138904, 5892092, 1695839}}}, 'Webprogrammeren en databases': {'lecture 1': {'day': 'Monday', 'timeslot': 9, 'room': 'A1.10', 'capacity': 56, 'max students': 1000, 'students': {10698627, 16333449, 72577292, 89180944, 69459473, 77392404, 5615125, 76648468, 39230359, 1137946, 67073567, 64228258, 78243495, 20618153, 28358060, 3474870, 27064249, 43902015, 43460038, 24891081, 41790793, 76903244, 57086672, 14847953, 53202517, 49908313, 72895450, 76123484, 33877725, 6249823, 66034145, 94930277, 22288615, 14303208, 17092717, 2416751, 61443567, 40434933, 53512831}}, 'lecture 2': {'day': 'Thursday', 'timeslot': 15, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {10698627, 16333449, 72577292, 89180944, 69459473, 77392404, 5615125, 76648468, 39230359, 1137946, 67073567, 64228258, 78243495, 20618153, 28358060, 3474870, 27064249, 43902015, 43460038, 24891081, 41790793, 76903244, 57086672, 14847953, 53202517, 49908313, 72895450, 76123484, 33877725, 6249823, 66034145, 94930277, 22288615, 14303208, 17092717, 2416751, 61443567, 40434933, 53512831}}, 'tutorial 1': {'day': 'Wednesday', 'timeslot': 13, 'room': 'A1.10', 'capacity': 56, 'max students': 20.0, 'students': {72577292, 69459473, 76648468, 67073567, 3474870, 27064249, 43460038, 24891081, 76903244, 57086672, 49908313, 72895450, 76123484, 33877725, 6249823, 66034145, 22288615, 2416751, 40434933, 53512831}}, 'tutorial 2': {'day': 'Wednesday', 'timeslot': 15, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {10698627, 16333449, 89180944, 77392404, 5615125, 39230359, 1137946, 64228258, 78243495, 20618153, 28358060, 43902015, 41790793, 14847953, 53202517, 94930277, 14303208, 17092717, 61443567}}, 'practical 1': {'day': 'Tuesday', 'timeslot': 11, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {72577292, 69459473, 77392404, 76648468, 39230359, 64228258, 78243495, 28358060, 3474870, 43902015, 57086672, 49908313, 72895450, 76123484, 33877725, 6249823, 66034145, 14303208, 61443567, 40434933}}, 'practical 2': {'day': 'Tuesday', 'timeslot': 11, 'room': 'A1.04', 'capacity': 41, 'max students': 20.0, 'students': {10698627, 16333449, 89180944, 5615125, 1137946, 67073567, 20618153, 27064249, 43460038, 24891081, 41790793, 76903244, 14847953, 53202517, 94930277, 22288615, 17092717, 2416751, 53512831}}}, 'Technology for games': {'lecture 1': {'day': 'Wednesday', 'timeslot': 11, 'room': 'C1.112', 'capacity': 60, 'max students': 1000, 'students': {36785409, 37110913, 11996292, 14309255, 97371272, 92496780, 77636749, 43680781, 4697362, 9332762, 47982619, 75664412, 12430748, 58565406, 10149535, 32204977, 14383795, 89338938, 31194811, 44901052, 26406342, 76487754, 68315599, 70336464, 69086548, 7106649, 6249823, 23547619, 22323043, 75521763, 85335143, 12077419, 77264363, 48308205, 21192048, 93041523, 41578612, 40434933}}, 'lecture 2': {'day': 'Tuesday', 'timeslot': 13, 'room': 'A1.10', 'capacity': 56, 'max students': 1000, 'students': {36785409, 37110913, 11996292, 14309255, 97371272, 92496780, 77636749, 43680781, 4697362, 9332762, 47982619, 75664412, 12430748, 58565406, 10149535, 32204977, 14383795, 89338938, 31194811, 44901052, 26406342, 76487754, 68315599, 70336464, 69086548, 7106649, 6249823, 23547619, 22323043, 75521763, 85335143, 12077419, 77264363, 48308205, 21192048, 93041523, 41578612, 40434933}}, 'tutorial 1': {'day': 'Tuesday', 'timeslot': 15, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {36785409, 37110913, 92496780, 77636749, 4697362, 47982619, 75664412, 32204977, 44901052, 76487754, 68315599, 70336464, 69086548, 6249823, 23547619, 85335143, 12077419, 21192048, 41578612, 40434933}}, 'tutorial 2': {'day': 'Tuesday', 'timeslot': 9, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {22323043, 11996292, 89338938, 26406342, 14309255, 97371272, 75521763, 77264363, 48308205, 43680781, 93041523, 14383795, 7106649, 9332762, 31194811, 12430748, 58565406, 10149535}}}, 'Project Genetic Algorithms': {'practical 1': {'day': 'Monday', 'timeslot': 15, 'room': 'B0.201', 'capacity': 48, 'max students': 15.0, 'students': {5526560, 25994016, 55480737, 8522855, 68409833, 14398123, 46701583, 69459473, 41578612, 82066165, 24613625, 76661016, 74361881, 78821918}}, 'practical 2': {'day': 'Thursday', 'timeslot': 11, 'room': 'A1.04', 'capacity': 41, 'max students': 15.0, 'students': {37770881, 75680261, 84449005, 27950803, 94467156, 51673172, 99283252, 86180471, 14179347, 66701209, 34773179, 27925117, 41644639}}, 'practical 3': {'day': 'Friday', 'timeslot': 9, 'room': 'A1.08', 'capacity': 20, 'max students': 15.0, 'students': {88737765, 76924297, 25077484, 87602030, 25106480, 58253841, 48678993, 87830198, 40633534}}}, 'Heuristieken 2': {'lecture 1': {'day': 'Wednesday', 'timeslot': 9, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {51566595, 5739011, 33760909, 58736785, 85236626, 1886996, 81022997, 81200278, 78243495, 63634350, 99975346, 84524083, 58040377, 670011, 31897288, 43027916, 16097870, 57086672, 52304977, 22731474, 48678993, 7106649, 82968410, 72652638, 83869542, 34765676, 87602030, 15249775, 5976174, 61443567, 35315956, 27925117}}, 'tutorial 1': {'day': 'Monday', 'timeslot': 13, 'room': 'A1.04', 'capacity': 41, 'max students': 20.0, 'students': {51566595, 78243495, 31897288, 61443567, 87602030, 15249775, 57086672, 52304977, 22731474, 85236626, 99975346, 81022997, 48678993, 58736785, 35315956, 7106649, 670011}}, 'tutorial 2': {'day': 'Thursday', 'timeslot': 13, 'room': 'A1.08', 'capacity': 20, 'max students': 20.0, 'students': {5739011, 83869542, 34765676, 33760909, 16097870, 63634350, 5976174, 43027916, 84524083, 1886996, 81200278, 58040377, 82968410, 27925117, 72652638}}}, 'Data Mining': {'lecture 1': {'day': 'Wednesday', 'timeslot': 13, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {45414528, 66122625, 37110913, 51566595, 19337738, 37744525, 25330192, 87314964, 81022997, 81200278, 13996448, 91196968, 52311353, 13116738, 68360259, 97136582, 99453514, 50143947, 21964491, 74131924, 93023961, 87900893, 98780382, 22323043, 59753700, 17823206, 70878567}}, 'lecture 2': {'day': 'Wednesday', 'timeslot': 13, 'room': 'A1.04', 'capacity': 41, 'max students': 1000, 'students': {45414528, 66122625, 37110913, 51566595, 19337738, 37744525, 25330192, 87314964, 81022997, 81200278, 13996448, 91196968, 52311353, 13116738, 68360259, 97136582, 99453514, 50143947, 21964491, 74131924, 93023961, 87900893, 98780382, 22323043, 59753700, 17823206, 70878567}}, 'tutorial 1': {'day': 'Wednesday', 'timeslot': 9, 'room': 'A1.06', 'capacity': 22, 'max students': 10.0, 'students': {37110913, 51566595, 19337738, 50143947, 99453514, 25330192, 74131924, 81022997, 81200278, 87900893}}, 'tutorial 2': {'day': 'Tuesday', 'timeslot': 11, 'room': 'A1.10', 'capacity': 56, 'max students': 10.0, 'students': {45414528, 68360259, 22323043, 70878567, 91196968, 21964491, 87314964, 93023961, 98780382}}, 'tutorial 3': {'day': 'Monday', 'timeslot': 9, 'room': 'B0.201', 'capacity': 48, 'max students': 10.0, 'students': {13996448, 66122625, 13116738, 59753700, 17823206, 97136582, 37744525, 52311353}}, 'practical 1': {'day': 'Thursday', 'timeslot': 11, 'room': 'B0.201', 'capacity': 48, 'max students': 10.0, 'students': {13996448, 22323043, 97136582, 70878567, 19337738, 50143947, 37744525, 87314964, 52311353, 98780382}}, 'practical 2': {'day': 'Thursday', 'timeslot': 15, 'room': 'A1.04', 'capacity': 41, 'max students': 10.0, 'students': {66122625, 37110913, 51566595, 59753700, 91196968, 21964491, 81200278}}, 'practical 3': {'day': 'Thursday', 'timeslot': 9, 'room': 'A1.04', 'capacity': 41, 'max students': 10.0, 'students': {45414528, 13116738, 68360259, 17823206, 99453514, 25330192, 74131924, 81022997, 93023961, 87900893}}}, 'Interactie-ontwerp': {'lecture 1': {'day': 'Monday', 'timeslot': 17, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {76924297, 44828429, 69634191, 81200278, 76661016, 64768422, 28055464, 38179241, 93566383, 81385263, 4546613, 3707829, 19214659, 20374340, 21677389, 14847953, 2550487, 37399898, 81155296, 66034145, 23547619, 34765676, 37701751, 65675896, 5368702}}, 'lecture 2': {'day': 'Thursday', 'timeslot': 15, 'room': 'B0.201', 'capacity': 48, 'max students': 1000, 'students': {76924297, 44828429, 69634191, 81200278, 76661016, 64768422, 28055464, 38179241, 93566383, 81385263, 4546613, 3707829, 19214659, 20374340, 21677389, 14847953, 2550487, 37399898, 81155296, 66034145, 23547619, 34765676, 37701751, 65675896, 5368702}}}, 'Autonomous Agents 2': {'lecture 1': {'day': 'Tuesday', 'timeslot': 15, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': {37110913, 51566595, 62872965, 22871048, 54026378, 52552718, 27298319, 36508571, 61611295, 19858730, 11915563, 5517869, 34806836, 88627897, 39459642, 72796858, 44901052, 16097870, 74131924, 70113753, 68409833, 62356458}}, 'lecture 2': {'day': 'Friday', 'timeslot': 15, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {37110913, 51566595, 62872965, 22871048, 54026378, 52552718, 27298319, 36508571, 61611295, 19858730, 11915563, 5517869, 34806836, 88627897, 39459642, 72796858, 44901052, 16097870, 74131924, 70113753, 68409833, 62356458}}, 'tutorial 1': {'day': 'Monday', 'timeslot': 9, 'room': 'C1.112', 'capacity': 60, 'max students': 10.0, 'students': {62872965, 62356458, 11915563, 19858730, 74131924, 88627897, 39459642, 36508571, 44901052, 61611295}}, 'tutorial 2': {'day': 'Monday', 'timeslot': 11, 'room': 'C0.110', 'capacity': 117, 'max students': 10.0, 'students': {68409833, 54026378, 5517869, 16097870, 52552718}}, 'tutorial 3': {'day': 'Thursday', 'timeslot': 13, 'room': 'A1.04', 'capacity': 41, 'max students': 10.0, 'students': {37110913, 51566595, 22871048, 27298319, 34806836, 70113753, 72796858}}, 'practical 1': {'day': 'Wednesday', 'timeslot': 13, 'room': 'A1.06', 'capacity': 22, 'max students': 10.0, 'students': {22871048, 62356458, 5517869, 16097870, 36508571, 44901052, 61611295}}, 'practical 2': {'day': 'Tuesday', 'timeslot': 13, 'room': 'A1.08', 'capacity': 20, 'max students': 10.0, 'students': {62872965, 54026378, 11915563, 74131924, 72796858, 70113753, 39459642}}, 'practical 3': {'day': 'Thursday', 'timeslot': 9, 'room': 'A1.06', 'capacity': 22, 'max students': 10.0, 'students': {37110913, 51566595, 68409833, 19858730, 52552718, 27298319, 34806836, 88627897}}}, 'Machine Learning': {'lecture 1': {'day': 'Wednesday', 'timeslot': 11, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {90067329, 23798155, 37744525, 46701583, 85236626, 33252501, 26857113, 2079771, 49683101, 67625383, 3685034, 15051051, 38296757, 39459642, 56988998, 40791377, 27187154, 94467156, 63111000, 61518436, 5976174, 77240949}}, 'lecture 2': {'day': 'Friday', 'timeslot': 17, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {90067329, 23798155, 37744525, 46701583, 85236626, 33252501, 26857113, 2079771, 49683101, 67625383, 3685034, 15051051, 38296757, 39459642, 56988998, 40791377, 27187154, 94467156, 63111000, 61518436, 5976174, 77240949}}}, 'Architectuur en computerorganisatie': {'lecture 1': {'day': 'Wednesday', 'timeslot': 15, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {23798155, 72577292, 13798030, 89180944, 59289233, 20331158, 14138904, 82689818, 49683101, 10149535, 28618400, 34872117, 70015932, 43460038, 72683344, 58866007, 29718115, 45556081, 40434933, 27925117, 83266686}}, 'lecture 2': {'day': 'Monday', 'timeslot': 9, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': {23798155, 72577292, 13798030, 89180944, 59289233, 20331158, 14138904, 82689818, 49683101, 10149535, 28618400, 34872117, 70015932, 43460038, 72683344, 58866007, 29718115, 45556081, 40434933, 27925117, 83266686}}}, 'Informatie- en organisatieontwerp': {'lecture 1': {'day': 'Tuesday', 'timeslot': 11, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': {23257088, 77636749, 36748818, 18266644, 19958553, 8557857, 11459236, 32204977, 44901052, 13116738, 13658563, 68315599, 29718115, 58332004, 75521763, 70878567, 17496687, 75585647, 62701040, 23983476, 92977271}}, 'lecture 2': {'day': 'Friday', 'timeslot': 9, 'room': 'A1.04', 'capacity': 41, 'max students': 1000, 'students': {23257088, 77636749, 36748818, 18266644, 19958553, 8557857, 11459236, 32204977, 44901052, 13116738, 13658563, 68315599, 29718115, 58332004, 75521763, 70878567, 17496687, 75585647, 62701040, 23983476, 92977271}}, 'tutorial 1': {'day': 'Wednesday', 'timeslot': 15, 'room': 'A1.06', 'capacity': 22, 'max students': 15.0, 'students': {8557857, 13116738, 29718115, 58332004, 11459236, 75521763, 68315599, 17496687, 75585647, 32204977, 18266644, 19958553}}, 'tutorial 2': {'day': 'Wednesday', 'timeslot': 11, 'room': 'A1.08', 'capacity': 20, 'max students': 15.0, 'students': {23257088, 13658563, 70878567, 77636749, 62701040, 36748818, 23983476, 92977271, 44901052}}, 'practical 1': {'day': 'Tuesday', 'timeslot': 15, 'room': 'C0.110', 'capacity': 117, 'max students': 15.0, 'students': {8557857, 13116738, 29718115, 58332004, 13658563, 75521763, 70878567, 77636749, 68315599, 17496687, 75585647, 62701040, 18266644, 23983476}}, 'practical 2': {'day': 'Tuesday', 'timeslot': 13, 'room': 'A1.06', 'capacity': 22, 'max students': 15.0, 'students': {23257088, 11459236, 32204977, 36748818, 92977271, 19958553, 44901052}}}, 'Advanced Heuristics': {'lecture 1': {'day': 'Friday', 'timeslot': 9, 'room': 'A1.10', 'capacity': 56, 'max students': 1000, 'students': {92665222, 60352393, 72577292, 1886996, 20883994, 28618400, 3168419, 62613937, 72665524, 27064249, 40633534, 78136904, 72683344, 14847953, 75997788, 23547619, 39429093, 70844780, 86807027, 47477884}}, 'practical 1': {'day': 'Tuesday', 'timeslot': 11, 'room': 'C1.112', 'capacity': 60, 'max students': 10.0, 'students': {28618400, 23547619, 78136904, 70844780, 72577292, 86807027, 1886996, 27064249, 75997788, 40633534}}, 'practical 2': {'day': 'Tuesday', 'timeslot': 9, 'room': 'A1.06', 'capacity': 22, 'max students': 10.0, 'students': {3168419, 39429093, 92665222, 60352393, 72683344, 62613937, 14847953, 72665524, 20883994, 47477884}}}, 'No course': {'No classes 1': {'day': 'Monday', 'timeslot': 9, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 2': {'day': 'Monday', 'timeslot': 11, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 3': {'day': 'Monday', 'timeslot': 13, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 4': {'day': 'Monday', 'timeslot': 15, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 5': {'day': 'Wednesday', 'timeslot': 11, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 6': {'day': 'Thursday', 'timeslot': 11, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 7': {'day': 'Thursday', 'timeslot': 13, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 8': {'day': 'Thursday', 'timeslot': 15, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 9': {'day': 'Friday', 'timeslot': 9, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 10': {'day': 'Friday', 'timeslot': 11, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 11': {'day': 'Friday', 'timeslot': 13, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 12': {'day': 'Friday', 'timeslot': 15, 'room': 'A1.06', 'capacity': 22, 'max students': 1000, 'students': set()}, 'No classes 13': {'day': 'Tuesday', 'timeslot': 9, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': set()}, 'No classes 14': {'day': 'Tuesday', 'timeslot': 11, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': set()}, 'No classes 15': {'day': 'Wednesday', 'timeslot': 17, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': set()}, 'No classes 16': {'day': 'Friday', 'timeslot': 13, 'room': 'C0.110', 'capacity': 117, 'max students': 1000, 'students': set()}}}

        self.student_id_dict = self.__init_student_schedule(schedule)
        self.course_dict = self.__init_course_schedule(schedule)
        self.room_dict = self.__init_room_schedule(schedule)

    def run(self) -> None:
        self.mainloop()

    def export(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()