
def change_students(df, course_list, Roster, num=10):
    student_list = find_worst_students(df, num)
    space_dict = find_space(course_list)
    # shuffle_students(student_list, space_dict, Roster)

def find_worst_students(df, num=10):
    df.sort_values(['Student Malus'], ascending=False, inplace=True)
    worst_students = df['Object'].unique()[:num]
    return worst_students

def find_space(course_list):

    space_dict = {}

    for course in course_list:
        max_tut = course.max_std
        max_pra = course.max_std_practica

        if max_tut > 1:

            for tutorial in course.tut_group_dict:

                space = int(max_tut - course.tut_group_dict[tutorial])

                if space > 0:

                    if course.name not in space_dict:
                        space_dict[course.name] = {}

                    space_dict[course.name][f'Tutorial {tutorial}'] = space

        if max_pra > 1:

            for practical in course.pract_group_dict:

                space = int(max_pra - course.pract_group_dict[practical])

                if space > 0:

                    if course.name not in space_dict:
                        space_dict[course.name] = {}

                    space_dict[course.name][f'Practical {practical}'] = space

    return space_dict

def shuffle_pra(class_indexes, student, course, space_dict, Roster):

    print('PRA')
    print(student.pract_group[course.name])
    print()

    for i in class_indexes:

        timeslot = student.timeslots[i]

        # if timeslot['class'].startswith('practical'):
            # student.timeslots.remove(timeslot)
    return



def shuffle_tut(class_indexes, student, course, space_dict, Roster):

    print('TUT')
    print(student.tut_group[course.name])
    print()

    free_tutorials = []
    for class_group in space_dict[course.name]:
        if class_group.startswith('Tutorial'):
            free_tutorials.append(class_group[-1])

    for i in class_indexes:

        timeslot = student.timeslots[i]


        if timeslot['class'].startswith('tutorial'):

            print(f'length of student timeslot list: {len(student.timeslots)}')

            student.timeslots.remove(timeslot)

            for tutorial in free_tutorials:

                print('MALUS POINTS')
                print(student.malus_count)

                student.tut_group[course.name] = tutorial
                timeslot_dict = student.tutorial_timeslot(course, Roster.schedule[course.name])
                student.timeslots.append(timeslot_dict)
                student.malus_points()
                student.timeslots.remove(timeslot_dict)

    return


def shuffle_students(student_list, space_dict, Roster):

    for student in student_list:
        print('\n=======\n')
        print(student.f_name)
        print(student.malus_count)
        print(student.timeslots)
        for course in student.courses:
            if course.name in space_dict:

                print('\n')
                print(course.name)

                class_indexes = []

                for i, timeslot in enumerate(student.timeslots):
                    if course.name in timeslot['course'] == course.name:
                        class_indexes.append(i)

                if course.name in student.tut_group:
                    shuffle_tut(class_indexes, student, course, space_dict, Roster)

                if course.name in student.pract_group:
                    shuffle_pra(class_indexes, student, course, space_dict, Roster)


                print()
                print('FREE')
                print(space_dict[course.name])

