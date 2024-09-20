import requests
import query as q
from tabulate import tabulate
import pandas as pd

fname = 'Jatish'
lname = 'Bhatia'
sub = 'COMP'
sub_num = '6741'
evt = 'Lab'
lec_num = '2'
topic = 'Knowledge Graph'
course = 'Intelligent Systems'
# query = q.topics_in_course_events(topic)


query = q.reading_for_topic_course(topic,course)

print(query)
        
response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
if response.status_code == 200:
    
    reading = [result['Course_Content_URI']['value'] for result in response.json()['results']['bindings']]
    reading_name = [result['Course_Content_Name']['value'] for result in response.json()['results']['bindings']]
    formatted_content = []

    for i in range(len(reading)):
        formatted_content.append(f"{reading_name[i]}, {reading[i]}")

    formatted_string = '\n'.join(formatted_content)
    
    if formatted_string:
        # reading_list = "\n".join(reading)
        print(f"Here is a list of readings for {course} :\n{formatted_string}")
    else:
        print("No content found for readings found for {course}.")