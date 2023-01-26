# This file simply puts the csv files into dataframes.

import pandas as pd

# put the csv files into Dataframes
COURSES = pd.read_csv('data/vakken.csv')
ROOMS = pd.read_csv('data/zalen.csv')
STUDENT_COURSES = pd.read_csv('data/studenten_en_vakken.csv')

if __name__ == "__main__":
    print(COURSES)
    print(ROOMS)
    print(STUDENT_COURSES)