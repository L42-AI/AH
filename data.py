# This file simply puts the csv files into dataframes.

import pandas as pd

# put the csv files into Dataframes
COURSES = pd.read_csv('vakken.csv')
ROOMS = pd.read_csv('zalen.csv')
STUDENT_COURSES = pd.read_csv('studenten_en_vakken.csv')

if __name__ == "__main__":
    print(COURSES)
    print(ROOMS)
    print(STUDENT_COURSES)