import requests

username = "gmrzone1"
password = "27021992samgalnote4"
base_url = "http://127.0.0.1:8000/api"

r = requests.get(f"{base_url}/courses/")

courses = r.json()

available_courses = ", ".join([course['title'] for course in courses])
print("Available Courses Are {0}".format(available_courses))


# course_list_with_content_endpoint = f"{base_url}/course_viewset/course_list_with_content"

# r = requests.get(course_list_with_content_endpoint, auth=(username, password))
# courses_with_content = r.json()
# print(courses_with_content)


#  Enroll user to all available Courses

for course in courses:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(f"{base_url}/course/enroll/{course_id}/", auth=(username, password))
    if r.json()['enrolled']:
        print("Sucessfully Enrolled {0}".format(course_title))