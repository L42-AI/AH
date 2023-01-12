def schedule_fill(roster, course_list):
    
    for course in course_list:

        # go over the number of lectures, tutorials and practicals needed
        for i in range(course.lectures):

            # check how many students will attend this lecture
            attending = course.expected
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