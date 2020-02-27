import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student

db_dir_path = tempfile.gettempdir()
print(db_dir_path)
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add_student(student):
    if(student.first_name == None or student.last_name == None):
        return 'You must provide both first name and last name', 405
	
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    #queries.append(query.grades == student.grades)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_student_by_id(student_id, subject):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student = Student.from_dict(student)
    if not subject:
        return student
	
    if subject in student.grades.keys():
        return student
		
def get_student_by_last_name(last_name):
    students = Query()
    #print(last_name)
    student = student_db.search(students.last_name == last_name)
    #print(student)
	
    if not student:
        return student

    student = student[0]
    student = Student.from_dict(student)
    #print(student)
    return student

def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student_db.remove(doc_ids=[int(student_id)])
    return student_id
