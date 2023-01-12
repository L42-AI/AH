from data import *


# print(STUDENT_COURSES.head())
list_courses = ['Vak1', 'Vak2', 'Vak3', 'Vak4', 'Vak5']
dict_count = {}

for _, row in STUDENT_COURSES.iterrows():
    for course in list_courses:
        if row[course] not in dict_count:
            dict_count[row[course]] = 0
        dict_count[row[course]] += 1


if __name__== "__main__":
    print(dict_count)
        