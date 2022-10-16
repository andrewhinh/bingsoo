# Import the Canvas class
import inspect
from canvasapi import Canvas
import requests

from pprint import pprint
import pytz
from datetime import datetime

from pdf2text import to_text

# Canvas API URL
API_URL_ENV = "https://ucmerced.instructure.com/"
# Canvas API key
API_KEY_ENV = "1101~26cptUnMTQ9cIC1OjL72cq1PxIrcak2nxrxPKlH2K06gGuZXWnHzgmpKWXLAxYTz"

def getSyllabuses(API_URL, API_KEY):
  canvas = Canvas(API_URL, API_KEY)
  courses = canvas.get_courses(enrollment_state="active")

  syllabuses = []
  for course in courses:
    # pprint(course.name)
    try:
      files = course.get_files()
      # print(files, course)
      for file in files:
        if 'syllabus' in file.display_name.lower():
          print(file.display_name, "file")
          pdf = requests.get(file.url)
          text = to_text(pdf)
          # open(f'./{file.display_name.lower()}', "wb").write(pdf.content)
          syllabuses.append(text)
    except:
      print("error", course)

  return syllabuses

def getAssignments(API_URL, API_KEY):
  canvas = Canvas(API_URL, API_KEY)
  courses = canvas.get_courses(enrollment_state="active")

  exams = []
  newString = ""
  for course in courses:
    try:
      courseAssignments = course.get_assignments()
      # pprint(courseAssignments)
      for assignment in courseAssignments:
        # print(type(assignment.attributes))
        # pprint(list(assignment.attributes))
        return_string = ""
        assignment_due_date = ""
        if assignment.due_at != None:
          # print(assignment, "assignment")
          assignment_due_date = datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%SZ")
          if assignment_due_date.date() > datetime.now().date():
              pst = pytz.timezone("US/Pacific")
              date_time = pytz.timezone('UTC').localize(assignment_due_date)
              date_time = date_time.astimezone(pst)
              date_time = date_time.strftime("%m/%d/%Y %H:%M")
              result = "Assignment: %s is due at: %s" %(assignment.name, date_time)
              return_string = return_string + result
              # if assignment.published is True:
              dueAt = pytz.timezone('UTC').localize(assignment_due_date).astimezone(pst).strftime("%H:%M %m/%d/%Y")
              if 'Midterm' in str(assignment) or 'Final' in str(assignment) or 'Exam' in str(assignment) or 'Test' in str(assignment): 
                exam = {"id": assignment.id, "name": assignment.name, "description": return_string, "course_id": course.name, "due_at": dueAt if dueAt else None, "type": "Exam"}
                exams.append(exam)
              elif 'Essay' in str(assignment):
                exam = {"id": assignment.id, "name": assignment.name, "description": assignment.description, "course_id": course.name, "due_at": dueAt if dueAt else None, "type": "Essay"}
                exams.append(exam)

    except Exception as Error:
      print("error2", Error)

  return exams
    
# syllabus = getSyllabuses(API_URL_ENV, API_KEY_ENV) 
# print(syllabus)
exams = getAssignments(API_URL_ENV, API_KEY_ENV)
# print(exams)
examText = ""
for assignment in exams:
  for k, item in assignment.items():
    examText += f'{k}\t{item}\n'


print(examText)