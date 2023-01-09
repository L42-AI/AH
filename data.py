import pandas as pd

COURSES = pd.read_csv('LecturesLesroosters/vakken.csv', header=0)
ROOMS = pd.read_csv('LecturesLesroosters/zalen.csv', header=0)
STUDENT_COURSES = pd.read_csv('LecturesLesroosters/studenten_en_vakken.csv', header=0)