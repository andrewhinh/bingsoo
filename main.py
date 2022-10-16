# Import the Canvas class
from canvasapi import Canvas
import requests

from pprint import pprint

# Canvas API URL
API_URL = "https://ucmerced.instructure.com/"
# Canvas API key
API_KEY = "1101~26cptUnMTQ9cIC1OjL72cq1PxIrcak2nxrxPKlH2K06gGuZXWnHzgmpKWXLAxYTz"



# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
# groups = canvas.get_announcements()
courses = canvas.get_courses(enrollment_state="active")
midterms = []
essays = []
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
        # open(f'./{file.display_name.lower()}', "wb").write(pdf.content)
        syllabuses += (file.url, course.name)
  except:
    print("error", course)
  # courseAssignments = course.get_assignments()
  # pprint(courseAssignments)
  # for assignment in courseAssignments:
  #   if 'Midterm' in str(assignment).lower(): 
  #     midterms.append(assignment)
  #   elif 'Essay' in str(assignment).lower():
  #     essays.append(assignment)
    
print(syllabuses)
# for midterm in midterms:
#   print(midterm.due_at, "midterm")

# for essay in essays:
#   print(essay.due_at, "essay")
# announcements = canvas.get_announcements(list(courses))
# for announcement in announcements:
#   pprint(announcement)

# print(courses)
# group = Group()
# groups = canvas.get_groups()
# print(groups)
# pprint(canvas.get_announcements(context_codes = courses))
# for course in courses:
#     print(type(course))
#     print(canvas.get_announcements(course))
    # pprint(course.get_gradebook_history_dates)
    # print()

# get_settings