
def count_students(dataframe):
    """This function Counts the amount of students enrolled for each course"""

    list_courses = ['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']
    dict_count = {}

    # loop over each row of the dataframe and set the count plus 1
    for _, row in dataframe.iterrows():
        for course in list_courses:
            course_str = str(row[course])

            if course_str != 'nan':
                
                # check if its in the dict, if not make a key and set value to 0
                if course_str not in dict_count:
                    dict_count[course_str] = 0

                # count the students
                dict_count[course_str] += 1
            
    return dict_count