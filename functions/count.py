def count_students(dataframe):
    """Counts the amount of students enrolled for each course"""

    list_courses = ['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']
    dict_count = {}

    # loop over each row of the dataframe and set the count plus 1
    for _, row in dataframe.iterrows():
        for course in list_courses:
            if row[course] not in dict_count and row[course] != 'nan':
                dict_count[row[course]] = 0
            dict_count[row[course]] += 1
    return dict_count
