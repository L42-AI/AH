def schedule_fill(roster, course_list):
    
    for course in course_list:

        # go over the number of lectures, tutorials and practicals needed
        for i in range(course.lectures):

            # check how many students will attend this lecture
            attending = course.enrolled
            roster.fill_schedule(course, "lecture", i + 1, attending)

        # outer loop is incase more than one tut per group
        ## in csv there is always one tut or pract, but we want to make the program scalable 
        for _ in range(course.tutorials):
            for i in range(course.tutorial_rooms):

                # check how many students will attend this tutorial
                attending = course.tut_group_dict[i + 1]
                roster.fill_schedule(course, "tutorial", i + 1, attending)

        for _ in range(course.practica):
            for i in range(course.practica_rooms):

                # check how many students will attend this practical
                attending = course.pract_group_dict[i + 1]
                roster.fill_schedule(course, "practical", i + 1, attending)
    fill_empty_slots(roster)

def fill_empty_slots(roster):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    # Set possible timeslots
    timeslots = [9, 11, 13, 15]
    roster.schedule["No course"] = {}
    i = 1
    for room in roster.rooms:
        for day in days:
            for timeslot in timeslots:
                if room.availability[day][timeslot]:
                    classes = f"No classes {i}"
                    place_in_schedule(roster, room, day, timeslot, "No course", classes)
                    i += 1
            if room.id == 'C0.110':
                if room.availability[day][17]:
                    classes = f"No classes {i}"
                    place_in_schedule(roster, room, day, 17, "No course", classes)
                    i += 1

def place_in_schedule(roster, room, day, timeslot, course_name, classes):

    # only need class if it is an actual lesson
    roster.schedule[course_name][classes] = {}
    roster.schedule[course_name][classes]['day'] = day
    roster.schedule[course_name][classes]['timeslot'] = timeslot
    roster.schedule[course_name][classes]['room'] = room.id

    room.availability[day][timeslot] = False
