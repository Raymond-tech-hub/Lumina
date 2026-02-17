import random
import JSON
import time

'''
A Time table generator 
'''

class Timetable:
    def __init__(self, classroom, teachers):
        self.classroom = classroom #Different classes 2 West, 2 Gamma etc
        self.teachers = teachers #teachers.json file path 
        
    def         