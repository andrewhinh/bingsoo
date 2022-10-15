# Import the Canvas class
from canvasapi import Canvas

# Canvas API URL
API_URL = "https://ucmerced.instructure.com/api/v1/courses/25052/assignment_groups?exclude_assignment_submission_types[]=wiki_page&exclude_response_fields[]=description&exclude_response_fields[]=rubric&include[]=assignments&include[]=discussion_topic&override_assignment_dates=true&per_page=50"
# Canvas API key
API_KEY = "p@$$w0rd"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)