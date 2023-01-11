import pandas as pd
import random

# List of classes
classes = ["math", "science", "history", "english"]

# List of rooms
rooms = ["room1", "room2", "room3", "room4"]

# List of timeslots
timeslots = ["9:00am-10:30am", "10:45am-12:15pm", "1:00pm-2:30pm", "2:45pm-4:15pm"]

# Dictionary to store the students in each class
students = {"math": ["student1", "student2", "student3"],
             "science": ["student4", "student5", "student6"],
             "history": ["student7", "student8", "student9"],
             "english": ["student10", "student11", "student12"]}

# Create an empty DataFrame to store the schedules
schedules = pd.DataFrame(columns=["student", "class", "room", "timeslot"])

# Iterate over classes
for class_ in classes:
    # Randomly select a room and timeslot for the class
    room = random.choice(rooms)
    timeslot = random.choice(timeslots)
    # Iterate over the students in the class
    for student in students[class_]:
        # Append a row to the DataFrame for the student's schedule
        schedules = schedules.append({"student": student, "class": class_, "room": room, "timeslot": timeslot}, ignore_index=True)

# Print schedules
print(schedules)
