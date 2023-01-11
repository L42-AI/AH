# import pandas as pd
# import random

# # List of classes
# classes = ["math", "science", "history", "english"]

# # List of rooms
# rooms = ["room1", "room2", "room3", "room4"]

# # List of timeslots
# timeslots = ["9:00am-10:30am", "10:45am-12:15pm", "1:00pm-2:30pm", "2:45pm-4:15pm"]

# # Dictionary to store the students in each class
# students = {"math": ["student1", "student2", "student3"],
#              "science": ["student4", "student5", "student6"],
#              "history": ["student7", "student8", "student9"],
#              "english": ["student10", "student11", "student12"]}

# # Create an empty DataFrame to store the schedules
# schedules = pd.DataFrame(columns=["student", "class", "room", "timeslot"])

# # Iterate over classes
# for class_ in classes:
#     # Randomly select a room and timeslot for the class
#     room = random.choice(rooms)
#     timeslot = random.choice(timeslots)
#     # Iterate over the students in the class
#     for student in students[class_]:
#         # Append a row to the DataFrame for the student's schedule
#         schedules = schedules.append({"student": student, "class": class_, "room": room, "timeslot": timeslot}, ignore_index=True)

# # Print schedules
# print(schedules)

import random

# List of students
students = ["student1", "student2", "student3", "student4", "student5", 
            "student6", "student7", "student8", "student9", "student10",
            "student11", "student12", "student13", "student14", "student15", 
            "student16", "student17", "student18", "student19", "student20",
            "student21", "student22", "student23", "student24", "student25", 
            "student26", "student27", "student28", "student29", "student30",
            "student31", "student32", "student33", "student34", "student35", 
            "student36", "student37", "student38", "student39", "student40",
            "student41", "student42"]

# Maximum number of students per group
max_group_size = 9

# Create a list to store the groups
groups = []

# Randomly select a group of students
random.shuffle(students)
first_group = random.sample(students, max_group_size)
groups.append(first_group)

# Divide the remaining students into groups
remaining_students = list(set(students) - set(first_group))
while len(remaining_students) > max_group_size:
    new_group = remaining_students[:max_group_size]
    groups.append(new_group)
    remaining_students = remaining_students[max_group_size:]

# Add the remaining students to the last group
groups.append(remaining_students)

# Print the groups
for i, group in enumerate(groups):
    print(f"Group {i+1}: {group}")

print(len(group[1]), group[-1])
for key in group:
    print(key)
    print(group[key])