from classes import *
from data import COURSES, ROOMS, STUDENT_COURSES
from assign import *

'''
**UPLOADEN**
git add main.py
git commit -m "nieuwe main" 
git push origin Jacob
'''


course_list, student_list, rooms = assign(COURSES, ROOMS, STUDENT_COURSES)
