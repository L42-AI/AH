
def change_students(df, course_list, Roster, num=10):
    student_list = find_worst_students(df, num)


    # find_space(course_list)

def find_worst_students(df, num=10):
    df.sort_values(['Student Malus'], ascending=True, inplace=True)
    worst_students = df['Student Object'].unique()[:10]
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
            # print('practica')
            # print(max_pra)
            # print(course.pract_group_dict)
            pass