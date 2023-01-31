
# import random


# class Mutate():
#     def __init__(self, df, course_list, student_list, Roster):
#         self.df = df
#         self.course_list = course_list
#         self.student_list = student_list
#         self.Roster = Roster
#         self.switched_student = None

#     def __find_worst_student(self):
#         """ This function returns the N worst students in terms of malus points """

#         worst_student = sorted(self.student_list, key=lambda obj: obj.malus_count)[:10]
#         return worst_student

#     def __find_random_student(self):
#         """ This function returns the N worst students in terms of malus points """

#         return random.choice(self.student_list)


#     def __students_to_shuffle(self, student_list):
#         """ This function goes through every student in the input list and shuffels them """

#         # For each student:
#         for student1 in student_list:

#             # Find a second student
#             for student2 in student_list:

#                 # Skip if the same student
#                 if student1 == student2:
#                     continue

#                 # For each course
#                 for course in student1.courses:

#                     # If course in other students course list
#                     if course in student2.courses:

#                         # Shuffle students
#                         self.__shuffle(course, student1, student2)

#     def __students_to_shuffle_random(self):
#         """ This function shuffles two random students """

#         # Set a value that is not equal to enter while loop
#         student1 = 'a'
#         student2 = 'b'

#         # While students are not equal
#         while student1 != student2:

#             # Randomly select students
#             student1 = random.choice(self.student_list)
#             student2 = random.choice(self.student_list)

#             # Randomly select a course from student1
#             course = random.choice(student1.courses)

#             # Skip if course not in other student
#             if course not in student2.courses:
#                 continue

#         # When different students found:
#         self.__shuffle(course, student1, student2)

#     def __shuffle(self, course, s1, s2):
#         """ This function shuffles two students classes """

#         def find_timeslots(course, s, class_type):
#             """ This local function returns the timeslot of the student """

#             # For each timeslot in the courses
#             for timeslot in s.timeslots[course.name]:
#                 if timeslot.startswith(class_type):
#                     return timeslot

#         # take a random class types to change
#         class_type = random.choice(['tutorial', 'practical'])

#         # Find timeslot
#         s1_timeslot = find_timeslots(course, s1, class_type)
#         s2_timeslot = find_timeslots(course, s2, class_type)

#         # Skip if equal
#         if s1_timeslot == s2_timeslot:
#             return

#         # Switch the timeslots
#         s1.timeslots[course.name][s2_timeslot] = s2.timeslots[course.name][s2_timeslot]
#         s2.timeslots[course.name][s1_timeslot] = s1.timeslots[course.name][s1_timeslot]

#         # Delete the old timeslots
#         s1.timeslots[course.name].pop(s1_timeslot)
#         s2.timeslots[course.name].pop(s2_timeslot)

#     def __set_type(self, course):

#         # take a random class types to change
#         class_type = random.choice(['tutorial', 'practical'])

#         if class_type == 'tutorial':
#             group_dict = course.tut_group_dict
#             max_std = course.max_std
#         else:
#             group_dict = course.pract_group_dict
#             max_std = course.max_std_practical

#         return class_type, group_dict, max_std

#     def __find_timeslots(self, course, s, class_type):
#         """ This local function returns the timeslot of the student """

#         # For each timeslot in the courses
#         for timeslot in s.timeslots[course.name]:
#             if timeslot.startswith(class_type):
#                 return timeslot

#     def __change_group(self, s):
#         """ This function shuffles two students classes """

#         course = random.choice(self.course_list)

#         while course.name not in list(s.timeslots.keys()):
#             course = random.choice(self.course_list)

#         # Set class type
#         class_type, group_dict, max_std = self.__set_type(course)

#         # Find timeslot
#         s_timeslot = self.__find_timeslots(course, s, class_type)

#         for classes in self.Roster.schedule[course.name]:
#             if classes.startswith(class_type):

#                 if self.Roster.schedule[course.name][s_timeslot] != self.Roster.schedule[course.name][classes] and group_dict[int(classes[-1])] < max_std:

#                     s.timeslots[course.name][classes] = self.Roster.schedule[course.name][classes]
#                     s.timeslots[course.name].pop(s_timeslot)

#                     group_dict[int(classes[-1])] += 1
#                     group_dict[int(s_timeslot[-1])] -= 1
#                     return


#     def change_student_group(self):

#         student = self.__find_random_student()

#         self.__change_group(student)


#     def swap_2_students(self):

#         switch_student_list = self.__find_worst_student()

#         self.__students_to_shuffle(switch_student_list)

#     def swap_2_students_random(self):

#         self.__students_to_shuffle_random()

#     def swap_lessons(self, lesson_type, empty):
#         """
#         This function swaps two of the same lesson_type with the help of two input variables. 
#         Lesson type is a string of they type of lesson for example tutorial.
#         The second variable is a boolean whether you want to swap with an empty room or not. If empty is set to Fals
#         you swap the lesson with a random other lesson. If it is True you swap with an empty room.
#         """

#         # check if you swap with an empty room or another course
#         if empty:
#             # pick a random course that does have one or more lessons of said type
#             random_course_1 = random.choice([c for c in self.course_list if getattr(c, f'{lesson_type}s') > 0])
            
#             all_lessons_random_2 = [key for key in self.Roster.schedule['No course'].keys()]

#             course_two = 'No course'
        
#         else:
#             # pick random lesson that has at leas one of the lesson type
#             random_course_1, random_course_2 = random.sample([c for c in self.course_list if getattr(c, f'{lesson_type}s') > 0], 2)
#             all_lessons_random_2 = [key for key in self.Roster.schedule[random_course_2.name].keys() if lesson_type in key]
#             course_two = random_course_2.name
        
#         # get all the tutorials in the course and get all the empty rooms
#         all_lessons_random_1 = [key for key in self.Roster.schedule[random_course_1.name].keys() if lesson_type in key]

#         # choose a random lecture of that course
#         lesson_1 = random.choice(all_lessons_random_1)
#         lesson_2 = random.choice(all_lessons_random_2)

#         # define in order to be easier to read and to be able to switch keys and values of the dict
#         dict_1 = self.Roster.schedule[random_course_1.name][lesson_1]
#         dict_2 = self.Roster.schedule[course_two][lesson_2]

#         # switch the times in the schedule roster
#         self.Roster.schedule[random_course_1.name][lesson_1] = dict(zip(dict_1, dict_2.values()))
#         self.Roster.schedule[course_two][lesson_2] = dict(zip(dict_2, dict_1.values()))

#     def swap_worst_student(self):

#         # find student with highest malus
#         self.switch_student = self.__find_worst_student()[0]
#         print(self.switch_student.id)

#         # pick a tutorial or practical to switch
#         course, class_type = self.__pract_or_tut()

#         # check if tut or pract group is needed
#         course_group_type, student_group = self.__type_detect(class_type, course)


#         # pick a group to switch to
#         groups = list(course_group_type.keys())
#         group_to_switch_to = random.choice(groups)

#         # check if student is not already in it
#         if group_to_switch_to != student_group:
#             # check if there is room, given the type of the class
#             if course_group_type[group_to_switch_to] < course.max_std and class_type == 'tut':
#                 course_group_type[group_to_switch_to] += 1
#                 course_group_type[student_group] -= 1
#                 self.switch_student.tut_group[course.name] = group_to_switch_to
#                 self.switch_student.student_timeslots(self.Roster)

#             if course_group_type[group_to_switch_to] < course.max_std_practica and class_type == 'pract':
#                 course_group_type[group_to_switch_to] += 1
#                 course_group_type[student_group] -= 1
#                 self.switch_student.pract_group[course.name] = group_to_switch_to
#                 self.switch_student.student_timeslots(self.Roster)

#     def swap_random_lessons(self, empty):

#         # check if you want to swap with an empty room or not
#         if empty:
#             # get one random course and all the empty room time slots
#             random_course_1 = random.choice(self.course_list)
#             all_lessons_random_2 = [key for key in self.Roster.schedule['No course'].keys()]
#             course_two = 'No course'

#         else:
#             # get two random courses
#             random_course_1, random_course_2 = random.sample(self.course_list, 2)
#             all_lessons_random_2 = list(self.Roster.schedule[random_course_2.name].keys())
#             course_two = random_course_2.name

#         # get all the lessons in that course
#         all_lessons_random_1 = list(self.Roster.schedule[random_course_1.name].keys())

#         # choose two random lessons
#         lesson_1 = random.choice(all_lessons_random_1)
#         lesson_2 = random.choice(all_lessons_random_2)

#         # define in order to be easier to read and to be able to switch keys and values of the dict
#         dict_1 = self.Roster.schedule[random_course_1.name][lesson_1]
#         dict_2 = self.Roster.schedule[course_two][lesson_2]

#         # switch the times in the schedule roster
#         self.Roster.schedule[random_course_1.name][lesson_1] = dict(zip(dict_1, dict_2.values()))
#         self.Roster.schedule[course_two][lesson_2] = dict(zip(dict_2, dict_1.values()))

#     def __pract_or_tut(self):
#         picked = False
#         while not picked:
#             # pick random if tut or pract should be switched
#             tut_or_pract = ['tut', 'pract']

#             class_type = random.choice(tut_or_pract)

#             # pick a random course that should switch
#             course = random.choice(self.switch_student.courses)

#             if course.tutorials > 0 and class_type == 'tut':
#                 picked = True
#             if course.practica > 0 and class_type == 'pract':
#                 picked = True
#         return course, class_type

#     def __type_detect(self, class_type, course):

#         if class_type == 'tut':
#             course_group_type = course.tut_group_dict
#             student_group = self.switch_student.tut_group[course.name]
#         else:
#             course_group_type = course.pract_group_dict
#             student_group = self.switch_student.pract_group[course.name]
#         return course_group_type, student_group

#     def __pract_or_tut(self):
#         picked = False
#         while not picked:
#             # pick random if tut or pract should be switched
#             tut_or_pract = ['tut', 'pract']

#             class_type = random.choice(tut_or_pract)
            

#             # pick a random course that should switch
#             course = random.choice(self.switch_student.courses)

#             if course.tutorials > 0 and class_type == 'tut':
#                 picked = True
#             if course.practica > 0 and class_type == 'pract':
#                 picked = True
#         return course, class_type

#     def __type_detect(self, class_type, course):

#         if class_type == 'tut':
#             course_group_type = course.tut_group_dict
#             student_group = self.switch_student.tut_group[course.name]
#         else:
#             course_group_type = course.pract_group_dict
#             student_group = self.switch_student.pract_group[course.name]
#         return course_group_type, student_group

#     def swap_timeslots(self):
#         worst_student = self.__find_worst_student()



# import classes.Algorithms.mutate as MutateClass
# import math
# import copy
# import random

# class __HillClimber():
#     def __init__(self, Roster, df, course_list, student_list, annealing=False):
#         self.roster_list = []
#         self.course_list = course_list
#         self.student_list = student_list
#         self.df = df
#         self.Roster = Roster
#         self.ANNEALING = annealing

#     def step_method(self, M):
#         pass
    
#     def get_name(self):
#         pass

#     def climb(self, T):

#         # set best roster and malus score
#         self.best_roster = self.Roster
#         self.best_malus_score = self.best_roster.malus_count

#         # append the original roster
#         self.roster_list.append(self.best_roster)

#         for _ in range(1):
#             self.rosters = []
            
#             # allow for more random mutations before score is calculated or not
#             if self.ANNEALING:
#                 outer_loop = 5
#                 T = 16
#             else:
#                 outer_loop = 50
#                 T = 1

#             for _ in range(outer_loop):
#                 if self.ANNEALING:
#                     T -= 3
#                 # make a deep copy, initiate the swapper with the right roster and change that roster
#                 self.current_roster = copy.deepcopy(self.best_roster)
                
#                 for _ in range(T):
#                     M = MutateClass.Mutate(self.df, self.course_list, self.student_list, self.current_roster)
#                     self.step_method(M)

#                 # calculate the maluspoints
#                 self.current_roster.total_malus(self.student_list)
#                 self.current_malus_points = self.current_roster.malus_count
#                 self.rosters.append(self.current_roster)

#             self.replace_roster(T)

#             self.roster_list.append(self.best_roster)
#             print(self.best_roster.malus_cause)
#         return self.best_roster

#     def replace_roster(self, T=None):
#         self.current_best_roster = min(self.rosters, key=lambda x: x.malus_count)
#         print(self.current_best_roster)
#         if self.best_malus_score > self.current_best_roster.malus_count:
#             self.best_roster = self.current_best_roster
#             self.get_name()

            

# class HC_LectureSwap(__HillClimber):
#     def step_method(self, M):
#         M.swap_random_lessons(True)
#         M.swap_random_lessons(False)
#     def get_name(self):
#         print('timeslot swapped')


# '''does not work now because studentlist is only one student'''
# # class HC_StudentSwapWorst(__HillClimber):
# #     def step_method(self, M):
# #         M.swap_2_students()
        
#     # def get_name(self):
#     #     print("students swapped random")

# # class HC_StudentSwapRandom(__HillClimber):
# #     def step_method(self, M):
# #         M.swap_2_students_random()
# #     def get_name(self):
# #         print("StS")

# class HC_StudentSwitch(__HillClimber):
#     def step_method(self, M):
#         M.change_student_group()
#     def get_name(self):
#         print('student switched')

# class HC_WorstStudentRandomGroup(__HillClimber):
#     '''swaps the worst student with a random tut or pract group.
#        If it is full, it will pick the worst student to swap with'''

#     def step_method(self, M):
#         M.swap_worst_student()

#     def get_name(self):
#         print("worst students")

# class Simulated_Annealing(__HillClimber):

#     def replace_roster(self, T):

#             if self.best_malus_score > self.current_malus_points:
#                 self.best_roster = self.current_roster
#                 self.best_malus_score = self.current_malus_points
            
#             else: 
#                 p = math.exp(- (self.best_malus_score - self.current_malus_points) / T)
#                 randint = random.random()
#                 if randint <= p:
#                     self.best_roster = self.current_roster
#                     self.best_malus_score = self.current_malus_points


# class SA_LectureSwap(Simulated_Annealing):
#     def step_method(self, M):
#         M.swap_2_lectures()

# class SA_StudentSwap(Simulated_Annealing):
#     def step_method(self, M):
#         M.swap_2_students()

# class SA_StudentSwapRandom(Simulated_Annealing):
#     def step_method(self, M):
#         M.swap_2_students_random()
#     def get_name(self):
#         print("StS")

# class SA_StudentSwitch(Simulated_Annealing):
#     def step_method(self, M):
#         M.change_student_group()



# [day] toegevoegd aan malus.cause[Classes Gap] in student file en roster file

# # def swap_lessons(self, lesson_type, empty):
#     #     """
#     #     This function swaps two of the same lesson_type with the help of two input variables. 
#     #     Lesson type is a string of they type of lesson for example tutorial.
#     #     The second variable is a boolean whether you want to swap with an empty room or not. If empty is set to Fals
#     #     you swap the lesson with a random other lesson. If it is True you swap with an empty room.
#     #     """

#     #     # check if you swap with an empty room or another course
#     #     if empty:
#     #         # pick a random course that does have one or more lessons of said type
#     #         random_course_1 = random.choice([c for c in self.course_list if getattr(c, f'{lesson_type}s') > 0])
            
#     #         all_lessons_random_2 = [key for key in self.Roster.schedule['No course'].keys()]

#     #         course_two = 'No course'
        
#     #     else:
#     #         # pick random lesson that has at leas one of the lesson type
#     #         random_course_1, random_course_2 = random.sample([c for c in self.course_list if getattr(c, f'{lesson_type}s') > 0], 2)
#     # #         all_lessons_random_2 = [key for key in self.Roster.schedule[random_course_2.name].keys() if lesson_type in key]
#     # #         course_two = random_course_2.name
        
#     #     # get all the tutorials in the course and get all the empty rooms
#     #     all_lessons_random_1 = [key for key in self.Roster.schedule[random_course_1.name].keys() if lesson_type in key]

#     # #     # choose a random lecture of that course
#     # #     lesson_1 = random.choice(all_lessons_random_1)
#     # #     lesson_2 = random.choice(all_lessons_random_2)

#     # #     # define in order to be easier to read and to be able to switch keys and values of the dict
#     # #     dict_1 = self.Roster.schedule[random_course_1.name][lesson_1]
#     # #     dict_2 = self.Roster.schedule[course_two][lesson_2]

#     #             self.worst_student.pract_group[course.name] = student_group
#     #             self.switch_student.pract_group[course.name] = group_to_switch_to
#     #             self.switch_student.student_timeslots(self.Roster)
#     #             self.worst_student.student_timeslots(self.Roster)

#     # def swap_worst_student(self):
#     #     '''method finds the student with the worst score and swaps either its pract or tut group
#     #        if it wants to place a student in a group that is full, it will swap it with the student
#     #        in that group that has the worst score'''

#     #     # find students with highest malus
#     #     self.switch_student = self.__find_worst_student()

#     #     # pick randomly one of the worst students
#     #     self.switch_student = random.choice(self.switch_student)


#     #     # pick a tutorial or practical to switch
#     #     course, class_type = self.__pract_or_tut()

#     #     # if there is no tut or practical, you cannot switch
#     #     if class_type == None:
#     #         return

#     #     # check if tut or pract group is needed
#     #     course_group_type, student_group = self.__type_detect(class_type, course)

#     #     # pick a group to switch to
#     #     groups = list(course_group_type.keys())

#     #     # if there is only one group, you cannot switch
#     #     if len(groups) == 1:
#     #         return

#     #     group_to_switch_to = random.choice(groups)

#     #     # check if student is not already in it
#     #     if group_to_switch_to != student_group:

#     #         # check if there is room, given the type of the class
#     #         if course_group_type[group_to_switch_to] < course.max_std and class_type == 'tut':
#     #             course_group_type[group_to_switch_to] += 1
#     #             course_group_type[student_group] -= 1
#     #             for student in self.student_list:
            
#     #                 if course in student.courses:
#     #                     if student.tut_group[course.name] == group_to_switch_to:
#     #                         self.worst_student = student
#     #                         continue

#     #             self.switch_student.tut_group[course.name] = group_to_switch_to

#     #             # Get the value of f'practical {group_to_switch_to}' in self.worst_student's timeslots dictionary
#     #             practical_group_to_switch_to_value = self.worst_student.timeslots[course.name][f'tutorial {group_to_switch_to}']

#     #             # Remove the key f'practical {student_group}' from self.switch_student's timeslots dictionary
#     #             del self.switch_student.timeslots[course.name][f'tutorial {student_group}']

#     #             # Add the key f'practical {student_group}' with the value of f'practical {group_to_switch_to}' in self.switch_student's timeslots dictionary
#     #             self.switch_student.timeslots[course.name][f'tutorial {group_to_switch_to}'] = practical_group_to_switch_to_value
                
#     #         elif course_group_type[group_to_switch_to] < course.max_std_practical and class_type == 'pract':
#     #             course_group_type[group_to_switch_to] += 1
#     #             course_group_type[student_group] -= 1
#     #             for student in self.student_list:
#     #                 if course in student.courses:
#     #                     if student.pract_group[course.name] == group_to_switch_to:
#     #                         self.worst_student = student
#     #                         continue
#     #             self.switch_student.pract_group[course.name] = group_to_switch_to

#     #             # Get the value of f'practical {group_to_switch_to}' in self.worst_student's timeslots dictionary
#     #             practical_group_to_switch_to_value = self.worst_student.timeslots[course.name][f'practical {group_to_switch_to}']

#     #             # Remove the key f'practical {student_group}' from self.switch_student's timeslots dictionary
#     #             del self.switch_student.timeslots[course.name][f'practical {student_group}']

#     #             # Add the key f'practical {student_group}' with the value of f'practical {group_to_switch_to}' in self.switch_student's timeslots dictionary
#     #             self.switch_student.timeslots[course.name][f'practical {group_to_switch_to}'] = practical_group_to_switch_to_value

#     #         # swap with a student if its full
#     #         elif course_group_type[group_to_switch_to] == course.max_std and class_type == 'tut':

#     #             # if full, swap with the worst student in the group
#     #             students_in_group = [student for student in course.enrolled_students if student.tut_group[course.name] == group_to_switch_to]
#     #             self.worst_student = min(students_in_group, key=lambda x: x.malus_count)
               

#     #             self.worst_student.tut_group[course.name] = student_group
#     #             self.switch_student.tut_group[course.name] = group_to_switch_to
#     #             self.Roster.init_student_timeslots(self.Roster.student_list)

#     #             # Get the value of f'practical {student_group}' in self.switch_student's timeslots dictionary
#     #             practical_student_group_value = self.switch_student.timeslots[course.name][f'tutorial {student_group}']
#     #             # Get the value of f'practical {group_to_switch_to}' in self.worst_student's timeslots dictionary
#     #             practical_group_to_switch_to_value = self.worst_student.timeslots[course.name][f'tutorial {group_to_switch_to}']

#     #             # Remove the key f'practical {student_group}' from self.switch_student's timeslots dictionary
#     #             del self.switch_student.timeslots[course.name][f'tutorial {student_group}']
#     #             # Remove the key f'practical {group_to_switch_to}' from self.worst_student's timeslots dictionary
#     #             del self.worst_student.timeslots[course.name][f'tutorial {group_to_switch_to}']

#     #             # Add the key f'practical {student_group}' with the value of f'practical {group_to_switch_to}' in self.switch_student's timeslots dictionary
#     #             self.switch_student.timeslots[course.name][f'tutorial {group_to_switch_to}'] = practical_group_to_switch_to_value
#     #             # Add the key f'practical {group_to_switch_to}' with the value of f'practical {student_group}' in self.worst_student's timeslots dictionary
#     #             self.worst_student.timeslots[course.name][f'tutorial {student_group}'] = practical_student_group_value
        
#     #         else:
#     #             # if full, swap with the worst student in the group
#     #             students_in_group = [student for student in course.enrolled_students if student.pract_group[course.name] == group_to_switch_to]
#     #             self.worst_student = min(students_in_group, key=lambda x: x.malus_count)
#     #             self.worst_student.pract_group[course.name] = student_group
#     #             self.switch_student.pract_group[course.name] = group_to_switch_to
#     #             self.Roster.init_student_timeslots(self.Roster.student_list)

#     #             # Get the value of f'practical {student_group}' in self.switch_student's timeslots dictionary
#     #             practical_student_group_value = self.switch_student.timeslots[course.name][f'practical {student_group}']
#     #             # Get the value of f'practical {group_to_switch_to}' in self.worst_student's timeslots dictionary
#     #             practical_group_to_switch_to_value = self.worst_student.timeslots[course.name][f'practical {group_to_switch_to}']

#     #             # Remove the key f'practical {student_group}' from self.switch_student's timeslots dictionary
#     #             del self.switch_student.timeslots[course.name][f'practical {student_group}']
#     #             # Remove the key f'practical {group_to_switch_to}' from self.worst_student's timeslots dictionary
#     #             del self.worst_student.timeslots[course.name][f'practical {group_to_switch_to}']

#     #             # Add the key f'practical {student_group}' with the value of f'practical {group_to_switch_to}' in self.switch_student's timeslots dictionary
#     #             self.switch_student.timeslots[course.name][f'practical {group_to_switch_to}'] = practical_group_to_switch_to_value
#     #             # Add the key f'practical {group_to_switch_to}' with the value of f'practical {student_group}' in self.worst_student's timeslots dictionary
#     #             self.worst_student.timeslots[course.name][f'practical {student_group}'] = practical_student_group_value


# # def __pract_or_tut(self):
#     #     picked = False
#     #     while not picked:
#     #         # pick random if tut or pract should be switched
#     #         tut_or_pract = ['tut', 'pract']

#     #         class_type = random.choice(tut_or_pract)

#     #         # pick a random course that should switch
#     #         course = random.choice(self.switch_student.courses)

#     #         if course.tutorials > 0 and class_type == 'tut':
#     #             picked = True
#     #         elif course.practicals > 0 and class_type == 'pract':
#     #             picked = True
#     #         else:
#     #             return [], None
#     #     return course, class_type

#     # def __type_detect(self, class_type, course):

#     #     if class_type == 'tut':
#     #         course_group_type = course.tut_group_dict
#     #         student_group = self.switch_student.tut_group[course.name]
#     #     else:
#     #         course_group_type = course.pract_group_dict
#     #         student_group = self.switch_student.pract_group[course.name]
#     #     return course_group_type, student_group


# import random

# class Mutate():
#     def __init__(self, course_list, student_list, Roster):
#         self.Roster = Roster

#         self.course_list = course_list
#         self.student_list = student_list

#         # Dict with student and course objects with one attribute as value
#         # Makes searching them based on that attribute faster
#         self.student_dict = {}
#         self.__create_student_id_dict()
#         self.course_dict = {}
#         self.__create_course_name_dict()

#     """ INIT """

#     def __create_student_id_dict(self):
#         '''create a dict with students.id as keys so students can be hashed when id is known'''
#         self.student_dict = {student.id: student for student in self.student_list}

#     def __create_course_name_dict(self):
#         '''create a dict with course.name as keys so courses can be hashed when name is known'''
#         self.course_dict = {course.name: course for course in self.course_list}

#     """ GET """

#     def __get_course_object(self, name):
#         '''return course object given its name'''
#         return self.course_dict.get(name)

#     def __get_student_object(self, id):
#         '''return student object given its id'''
#         return self.student_dict.get(id)


#     """ METHODS """

#     """ Helpers """

#     def __find_random_student(self):
#         """ This function returns a random student from the students set"""

#         return random.choice(self.student_list)

#     def __students_to_shuffle(self):
#         """ This function shuffles two random students """

#         # Set arbitrary values to enter while loop
#         course_picked = False
#         student1 = 'a'
#         student2 = 'a'

#         # While students are not equal and course is not picked
#         while student1 == student2 or course_picked == False:

#             # Reset course picked boolean
#             course_picked = False

#             # Randomly select students
#             student1 = self.__find_random_student()
#             student2 = self.__find_random_student()

#             # Find the courses that both students follow
#             intersecting_courses = list(set(student1.courses) & set(student2.courses))

#             # Skip if no common courses are found
#             if len(intersecting_courses) == 0:
#                 continue

#             # Randomly select a course from possible courses
#             course = random.choice(intersecting_courses)

#             if course.tutorials + course.practicals > 0:
#                 course_picked = True

#         # When different students found:
#         self.__shuffle(course, student1, student2)
#         return

#     def __shuffle(self, course, s1, s2):
#         """ This function shuffles two students classes """

#         switched = False
#         tut_same = False
#         pract_same = False
#         while switched == False:

#             # take a random class types to change
#             if course.tutorials == 0:
#                 class_type = 'practical'

#                 if pract_same == True:
#                     switched = True
#             elif course.practicals == 0:
#                 class_type = 'tutorial'

#                 if tut_same == True:
#                     switched = True
#             else:
#                 class_type = random.choice(['tutorial', 'practical'])

#                 if tut_same and pract_same == True:
#                     switched = True

#             if class_type == 'tutorial':
#                 if s1.tut_group[course.name] == s2.tut_group[course.name]:
#                     tut_same = True
#                     continue
#                 else:
#                     s1_group = s1.tut_group[course.name]
#                     s2_group = s2.tut_group[course.name]

#                     s1.tut_group[course.name] = s2_group
#                     s2.tut_group[course.name] = s1_group

#             elif class_type == 'practical':
#                 if s1.pract_group[course.name] == s2.pract_group[course.name]:
#                     pract_same = True
#                     continue
#                 else:
#                     s1_group = s1.pract_group[course.name]
#                     s2_group = s2.pract_group[course.name]
#                     s1.pract_group[course.name] = s2_group
#                     s2.pract_group[course.name] = s1_group

#             switched = True

#     """ Method 1 """

#     def swap_2_students(self):

#         self.__students_to_shuffle()

#     """ Method 2 """

#     def swap_random_lessons(self, empty):

#         random_course_1, random_course_2 = self._get_course(empty)

#         # check if you want to swap with an empty room or not
#         if empty:
#             all_lessons_random_2 = [key for key in self.Roster.schedule['No course'].keys()]
#             random_course_2 = 'No course'

#         else:
#             # get two random courses
#             all_lessons_random_2 = list(self.Roster.schedule[random_course_2.name].keys())
#             random_course_2 = random_course_2.name

#         # get all the lessons in that course
#         all_lessons_random_1 = list(self.Roster.schedule[random_course_1.name].keys())

#         # choose two random lessons
#         lesson_1 = random.choice(all_lessons_random_1)
#         lesson_2 = random.choice(all_lessons_random_2)

#         # define in order to be easier to read and to be able to switch keys and values of the dict
#         dict_1 = self.Roster.schedule[random_course_1.name][lesson_1]
#         dict_2 = self.Roster.schedule[random_course_2][lesson_2]

#         # switch the times in the schedule roster
#         self.Roster.schedule[random_course_1.name][lesson_1] = dict(zip(dict_1, dict_2.values()))
#         self.Roster.schedule[random_course_2][lesson_2] = dict(zip(dict_2, dict_1.values()))

#     """ Helpers """
    
#     def _get_course(self, empty):
#         if empty:
#             random_course_1 = random.choice(self.course_list)
#             random_course_2 = None
#         else:
#             # get two random courses
#             random_course_1, random_course_2 = random.sample(self.course_list, 2)
#         return random_course_1, random_course_2

#     def __worst_day(self, student_to_switch):
#         '''finds worst day in the schedule of a student'''

#         worst_score = 0
#         worst_day = None

#         # go over the timeslot and find day with most gap hour
#         for day in student_to_switch.malus_cause['Classes Gap']:
#             if student_to_switch.malus_cause['Classes Gap'][day] > worst_score:
#                 worst_day = day
#         if worst_day == None:

#             # when worst_day is None, the main method will stop because no classes later on can be found
#             return 
#         return worst_day

#     def __find_classes(self, student_to_switch, worst_day):
#         '''picks the class that a student has on his/hers day with most malus points'''

#         classes = []
#         courses = []
#         for course in student_to_switch.timeslots:
#             for class_moment in student_to_switch.timeslots[course]:

#                 if student_to_switch.timeslots[course][class_moment]['day'] == worst_day:
#                     # check if it is tut or pract, not a lecture
#                     if class_moment[0] == 't' or class_moment[0] == 'p':
#                         classes.append(class_moment)
#                         courses.append(course)

#         # pick a random class
#         if len(classes) == 0:
#             return None, None
#         class_to_switch = random.choice(classes)
#         course = courses[classes.index(class_to_switch)]

#         # get the course object
#         course = self.__get_course_object(course)

#         return class_to_switch, course

#     def __tut_or_pract_for_bad_timeslot(self, course, student, t=True):
#         '''returns variable names for tutorial groups or practical groups'''

#         if t:
#             return course.tutorial_rooms, course.tut_group_dict, course.max_std, student.tut_group
#         else:
#             return course.practical_rooms, course.pract_group_dict, course.max_std_practical, student.pract_group

#     def __pick_group(self, course, course_group_dict, student_to_switch_group):
#         '''picks a group where a student who needs to swap tutorial or practical groups can go to'''

#         picked = False
#         while not picked:

#             # pick a group to switch to
#             groups = list(course_group_dict.keys())
#             new_group = random.choice(groups)
#             if new_group != student_to_switch_group[course.name]:
#                 picked = True
#         return new_group

#     """ Method 3 """

#     def swap_bad_timeslots(self):

#         # pick a student to switch
#         student_to_switch = self.__find_random_student()

#         # find its worst day
#         worst_day = self.__worst_day(student_to_switch)

#         # find classes that day
#         class_to_switch, course = self.__find_classes(student_to_switch, worst_day)

#         # stop if there are no good classes to switch
#         if class_to_switch == None:
#             return

#         # check the type of class
#         if class_to_switch[:8] == 'tutorial':
#             course_rooms, course_group_dict, course_max_std, student_to_switch_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch, t=True)
#         else:
#             course_rooms, course_group_dict, course_max_std, student_to_switch_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch, t=False)

#         # cannot switch if there are no or one classes of particular type
#         if course_rooms <= 1:
#             return

#         # pick a new group
#         new_group = self.__pick_group(course, course_group_dict, student_to_switch_group)

#         # check if there is room, given the type of the class
#         if course_group_dict[new_group] < course_max_std:
#             course_group_dict[new_group] += 1
#             course_group_dict[student_to_switch_group[course.name]] -= 1
#             student_to_switch_group[course.name] = new_group

#             # compute new malus for the student
#             student_to_switch.compute_malus(self.Roster.schedule)

#             # find the student object to replace with the same student that has new timeslot
#             student = self.__get_student_object(student_to_switch.id)
#             student = student_to_switch
#         else:

#             #  if full, swap with the worst student in the group
#             if class_to_switch[:8] == 'tutorial':
#                 students_in_group = [student for student in course.enrolled_students if student.tut_group[course.name] == new_group]
#             else:
#                 students_in_group = [student for student in course.enrolled_students if student.pract_group[course.name] == new_group]

#             # Find student to switch based on the highest malus
#             student_to_switch_new_group = max(students_in_group, key=lambda x: x.malus_count)

#             # set variables for new student
#             if class_to_switch[:8] == 'tutorial':
#                 course_rooms, course_group_dict, course_max_std, student_new_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch_new_group, t=True)
#             else:
#                 course_rooms, course_group_dict, course_max_std, student_new_group = self.__tut_or_pract_for_bad_timeslot(course, student_to_switch_new_group, t=False)

#             # swap students
#             student_new_group[course.name] = student_to_switch_group[course.name]
#             student_to_switch_group[course.name] = new_group

#             # make new timeslots for the students
#             student_to_switch_new_group.student_timeslots(self.Roster.schedule)
#             student_to_switch.student_timeslots(self.Roster.schedule)

#             # compute new malus for the student
#             student_to_switch.compute_malus(self.Roster.schedule)
#             student_to_switch_new_group.compute_malus(self.Roster.schedule)

#             # compute new malus for the student
#             student_to_switch.compute_malus(self.Roster.schedule)

#             # find the student object to replace with the same student that has new timeslot
#             student = self.__get_student_object(student_to_switch.id)
#             student = student_to_switch

#             student = self.__get_student_object(student_to_switch_new_group.id)
#             student = student_to_switch_new_group


# class Mutate_double_classes(Mutate):
#     def __worst_day(self, student_to_switch):
#         '''finds worst day in the schedule of a student'''

#         worst_score = 0
#         worst_day = None

#         # go over the timeslot and find day with most gap hour
#         for day in student_to_switch.malus_cause['Dubble Classes']:
#             if student_to_switch.malus_cause['Dubble Classes'][day] > worst_score:
#                 worst_day = day
#         if worst_day == None:
            
#             # when worst_day is None, the main method will stop because no classes later on can be found
#             return None
#         return worst_day
    
   
   
# class Mutate_Course_Swap_Capacity(Mutate):
#     def _get_course(self, empty):
#         if empty:
#             random_course_1 = self.Roster.course_capacity_malus_sorted[0]
#             random_course_2 = None
#         else:
#             # get two random courses
#             random_course_1 = self.Roster.course_capacity_malus_sorted[0]
#             picked = False
#             while not picked:
#                 random_course_2 = random.choice(self.course_list)
#                 if random_course_2.name != random_course_1.name:
#                     picked = True
#         return random_course_1, random_course_2


# import classes.Algorithms.mutate as MutateClass
# import copy
# import random


# """ Main HillClimber Class """

# class HillClimber():
#     def __init__(self, Roster, course_list, student_list):
#         self.roster_list = []
#         self.course_list = course_list
#         self.student_list = student_list
#         self.Roster = Roster

#     """ Inheritable methods """

#     def step_method(self, M):
#         pass

#     def get_name(self):
#         pass

#     def make_mutate(self):
#         M = MutateClass.Mutate(self.course_list, self.student_list, self.current_roster)
#         return M

#     def replace_roster(self, T=None):
#         self.current_best_roster = min(self.rosters, key=lambda x: x.malus_count)

#         if self.best_malus_score > self.current_best_roster.malus_count:
#             self.best_roster = self.current_best_roster

#     """ Main Method """

#     def climb(self):

#         performance = {self.get_name():[]}

#         # Set input roster as best roster and best malus count
#         self.best_roster = self.Roster
#         self.best_malus_score = self.best_roster.malus_count

#         # Append the input roster
#         self.roster_list.append(self.best_roster)

#         # Take 30 steps:
#         for _ in range(50):

#             # Make a deep copy, initiate the swapper with the right roster and change that roster
#             self.current_roster = copy.deepcopy(self.best_roster)

#             # Create the mutate class
#             M = self.make_mutate()

#             # Take a step
#             self.step_method(M)

#             # Set changed student list to roster student list
#             self.current_roster.student_list = M.student_list

#             # Calculate the maluspoints
#             self.current_roster.init_student_timeslots(self.current_roster.student_list)
#             self.current_roster.total_malus(self.student_list)

#             # Set malus points
#             self.current_malus_points = self.current_roster.malus_count

#             performance[self.get_name()].append(0)

#             # Compare with prior malus points
#             if self.best_malus_score > self.current_malus_points:
#                 performance[self.get_name()].append(self.best_malus_score - self.current_malus_points)
#                 self.best_roster = self.current_roster
#                 self.best_malus_score = self.current_malus_points

#                 # Print method name
#                 # print(self.get_name())

#         # Print new malus
#         # print(self.best_roster.malus_cause)

#         # Return new roster
#         return self.best_roster, performance

# """ Inherited HillClimber Classes """

# """ Step method bestaat niet meer, zit in lecture swap? """
# # class HC_LectureLocate(HillClimber):

# #     def step_method(self, M):
# #         M.swap_lecture_empty_room()

# class HC_TimeSlotSwapRandom(HillClimber):
#     '''swaps a random class with another random class'''
#     def step_method(self, M):

#         # Take a random state to pass to function
#         state = random.choice((True, False))
#         M.swap_random_lessons(state)

#     def get_name(self):
#         return "TimeSlotSwapRandom"

# class HC_TimeSlotSwapCapacity(HC_TimeSlotSwapRandom):
#     '''swaps the class that has the most capacity malus points with a random class'''
#     def make_mutate(self):
#         M = MutateClass.Mutate_Course_Swap_Capacity(self.course_list, self.student_list, self.current_roster)
#         return M

#     def get_name(self):
#         return "TimeSlotSwapCapacity"

# class HC_StudentSwap(HillClimber):

#     def step_method(self, M):
#         M.swap_2_students()

#     def get_name(self):
#         return "StudentSwap"

# class HC_SwapBadTimeslots_GapHour(HillClimber):
#     '''This class takes a random student and finds the day with the most gap hours.
#        When found, it will swap one tut or pract with a student from a different group
#        that has the most malus points from that group'''

#     def step_method(self, M):
#         M.swap_bad_timeslots()

#     def get_name(self):
#         return 'SwapBadTimeslots_GapHour'

# class HC_SwapBadTimeslots_DoubleClasses(HillClimber):
#     '''This class takes a random student and finds the day with the most double classes.
#        When found, it will swap one tut or pract with a student from a different group
#        that has the most malus points from that group'''

#     def make_mutate(self):
#         M = MutateClass.Mutate_double_classes(self.course_list, self.student_list, self.current_roster)
#         return M

#     def step_method(self, M):
#         M.swap_bad_timeslots()

#     def get_name(self):
#         return 'SwapBadTimeslots_DoubleClasses'

 # genetic_schedules = [copy.deepcopy(self.schedule) for _ in range(32)]

                # with Pool(4) as p:
                #     self.output_schedules = p.map(self.run_HC, [(0, genetic_schedules[0], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[1], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[2], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[3], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[4], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[5], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[6], T, self.hillclimber_counter),
                #                                                 (0, genetic_schedules[7], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[8], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[9], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[10], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[11], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[12], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[13], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[14], T, self.hillclimber_counter),
                #                                                 (1, genetic_schedules[15], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[16], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[17], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[18], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[19], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[20], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[21], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[22], T, self.hillclimber_counter),
                #                                                 (2, genetic_schedules[23], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[24], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[25], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[26], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[27], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[28], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[29], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[30], T, self.hillclimber_counter),
                #                                                 (3, genetic_schedules[31], T, self.hillclimber_counter)])

  # with Pool(4) as p:
                                # self.output_schedules = p.map(self.run_HC, [(0, schedules[0], T, self.hillclimber_counter),
                                #                                             (0, schedules[0], T, self.hillclimber_counter),
                                #                                             (0, schedules[1], T, self.hillclimber_counter),
                                #                                             (0, schedules[1], T, self.hillclimber_counter),
                                #                                             (0, schedules[2], T, self.hillclimber_counter),
                                #                                             (0, schedules[2], T, self.hillclimber_counter),
                                #                                             (0, schedules[3], T, self.hillclimber_counter),
                                #                                             (0, schedules[3], T, self.hillclimber_counter),
                                #                                             (1, schedules[0], T, self.hillclimber_counter),
                                #                                             (1, schedules[0], T, self.hillclimber_counter),
                                #                                             (1, schedules[1], T, self.hillclimber_counter),
                                #                                             (1, schedules[1], T, self.hillclimber_counter),
                                #                                             (1, schedules[2], T, self.hillclimber_counter),
                                #                                             (1, schedules[2], T, self.hillclimber_counter),
                                #                                             (1, schedules[3], T, self.hillclimber_counter),
                                #                                             (1, schedules[3], T, self.hillclimber_counter),
                                #                                             (2, schedules[0], T, self.hillclimber_counter),
                                #                                             (2, schedules[0], T, self.hillclimber_counter),
                                #                                             (2, schedules[1], T, self.hillclimber_counter),
                                #                                             (2, schedules[1], T, self.hillclimber_counter),
                                #                                             (2, schedules[2], T, self.hillclimber_counter),
                                #                                             (2, schedules[2], T, self.hillclimber_counter),
                                #                                             (2, schedules[3], T, self.hillclimber_counter),
                                #                                             (2, schedules[3], T, self.hillclimber_counter),
                                #                                             (3, schedules[0], T, self.hillclimber_counter),
                                #                                             (3, schedules[0], T, self.hillclimber_counter),
                                #                                             (3, schedules[1], T, self.hillclimber_counter),
                                #                                             (3, schedules[1], T, self.hillclimber_counter),
                                #                                             (3, schedules[2], T, self.hillclimber_counter),
                                #                                             (3, schedules[2], T, self.hillclimber_counter),
                                #                                             (3, schedules[3], T, self.hillclimber_counter),
                                #                                             (3, schedules[3], T, self.hillclimber_counter)])


            #                     if mode == 'solo':
            #     activation = random.choice([1,2,3,4])

            #     if activation == 1:
            #         HC1.schedule = self.schedule
            #         HC1.iteration = self.hillclimber_counter

            #         self.schedule, self.malus, self.hillclimber_counter = HC1.climb(T)


            #         # print(self.malus)

            #     elif activation == 2:
            #         HC2.schedule = self.schedule
            #         HC2.iteration = self.hillclimber_counter

            #         self.schedule, self.malus, self.hillclimber_counter = HC2.climb(T)


            #         # print(self.malus)

            #     elif activation == 3:
            #         HC3.schedule = self.schedule
            #         HC3.iteration = self.hillclimber_counter

            #         self.schedule, self.malus, self.hillclimber_counter = HC3.climb(T)


            #         # print(self.malus)

            #     elif activation == 4:
            #         HC4.schedule = self.schedule
            #         HC4.iteration = self.hillclimber_counter
            #         HC4.hillclimber_iterations = 1

            #         self.schedule, self.malus, self.hillclimber_counter = HC4.climb(T)

            #         # print(self.malus)
            # elif mode == 'multi':

            #     core_assignment_list = [0,1,1,2]

            #     with Pool(4) as p:
            #         self.output_schedules = p.map(self.run_HC, [(core_assignment_list[0], T, 1),
            #                                                     (core_assignment_list[1], T, 2),
            #                                                     (core_assignment_list[2], T, 3),
            #                                                     (core_assignment_list[3], T, 4)])
            #     # find the lowest malus of the output rosters
            #     min_malus = min([i[1]['Total'] for i in self.output_schedules])

            #     # Use the lowest malus to find the index of the best roster
            #     self.best_index = [i[1]['Total'] for i in self.output_schedules].index(min_malus)

            #     self.hillclimber_counter = self.output_schedules[0][3]

            #     # Compute difference between new roster and current roster
            #     difference = self.malus['Total'] - self.output_schedules[self.best_index][1]['Total']

            #     # replace the roster if it is better
            #     self.__replace_roster(difference)
            #     self.multiprocessor_counter += 1