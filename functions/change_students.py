
def change_students(df, course_list, num=10):
    student_list = find_worst_students(df, num)
    find_space(course_list)

def find_worst_students(df, num=10):
    df.sort_values(['Student Malus'], ascending=True, inplace=True)
    worst_students = df['Object'].unique()[:10]
    return worst_students

def find_space(course_list):
    for course in course_list:
        max_tut = course.max_std
        max_pra = course.max_std_practica
        print()
        print(course)
        print(course.enrolled)
        print()
        if max_tut > 1:
            print('tutorial')
            print(max_tut)
            for tutorial in course.tut_group_dict:
                course.tut_group_dict[tutorial]
        if max_pra > 1:
            print('practica')
            print(max_pra)
            print(course.pract_group_dict)

