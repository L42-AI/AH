import pandas as pd

COURSES = pd.read_csv('vakken.csv')
ROOMS = pd.read_csv('zalen.csv')
STUDENT_COURSES = pd.read_csv('studenten_en_vakken.csv')

if __name__ == "__main__":
    print(COURSES)
    print(ROOMS)
    print(STUDENT_COURSES)