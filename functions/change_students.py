
def change_students(df, course_list, num=10):
    student_list = find_worst_students(df, num)
    space_dict = find_space(course_list)
    # shuffle_students(student_list, space_dict)

def find_worst_students(df, num=10):
    df.sort_values(['Student Malus'], ascending=True, inplace=True)
    worst_students = df['Object'].unique()[:10]
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

def shuffle_students(student_list, space_dict):
    for student in student_list:
        for course in student.courses:
            if course.name in space_dict:
                print('=======')
                print(student.f_name)
                print(course.name)
                print()
                print('tut')
                print(student.tut_group)
                print('prac')
                print(student.pract_group)
                print()
                print(space_dict[course.name])

