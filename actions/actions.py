# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from KB_Construction import query as q
import requests
from tabulate import tabulate
import pandas as pd
from typing import Any, Text, Dict, List


#Query1
class UniversityInfo(Action):

    def name(self):
        return "course_by_uni"

    def run(self, dispatcher, tracker, domain):
        uni = tracker.get_slot('uni')
        print(uni)
      
        query = q.courses_by_uni(uni)
       
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            courses = [result['Course_Name']['value'] for result in response.json()['results']['bindings']]
            if courses:
                course_list = "\n".join(courses)
                dispatcher.utter_message(text=f"Here are the courses offered by {uni}:\n{course_list}")
            else:
                dispatcher.utter_message(text=f"No courses found for {uni}.")
        else:
            dispatcher.utter_message(text="Failed to fetch course information from the database.")
#Query2
class CourseDiscussedTopic(Action):

    def name(self):
        return "course_discussed_topic"

    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot('topic')
       
        print(topic)
      
        query = q.course_discussed_topic(topic)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            courses = [result['Course_Name']['value'] for result in response.json()['results']['bindings']]
            if courses:
                course_list = "\n".join(courses)
                dispatcher.utter_message(text=f"Here are the courses which discuss {topic}:\n{course_list}")
            else:
                dispatcher.utter_message(text=f"No courses found for {topic}.")
        else:
            dispatcher.utter_message(text="Failed to fetch course information from the database.")
#Query3
class TopicsInCourseLec(Action):

    def name(self):
        return "topics_in_course_lec"

    def run(self, dispatcher, tracker, domain):
        course = tracker.get_slot('course')
        lec = tracker.get_slot('lecture')
       
        print(course)
        print(lec)
      
        query = q.topics_in_course_lec(course,lec)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            topics = [result['Topic_Name']['value'] for result in response.json()['results']['bindings']]
            if topics:
                course_list = "\n".join(topics)
                dispatcher.utter_message(text=f"Here are the topics discussed in lecture {lec} in {course}:\n{course_list}")
            else:
                dispatcher.utter_message(text=f"No topics found for lecture {lec} in {course}.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")
#Query4
class CoursesByUniSubject(Action):

    def name(self):
        return "courses_by_uni_subject"

    def run(self, dispatcher, tracker, domain):
        uni = tracker.get_slot('uni')
        sub = tracker.get_slot('subject')
       
        print(uni)
        print(sub)
      
        query = q.courses_by_uni_subject(uni,sub)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            courses = [result['Course_Name']['value'] for result in response.json()['results']['bindings']]
            if courses:
                course_list = "\n".join(courses)
                dispatcher.utter_message(text=f"Here are the courses covered by {uni} in subject {sub} :\n{course_list}")
            else:
                dispatcher.utter_message(text=f"No course found for {sub} in {uni}.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")
#Query5
class MaterialTopicInCourse(Action):

    def name(self):
        return "material_topic_in_course"

    def run(self, dispatcher, tracker, domain):
        sub_num = tracker.get_slot('sub_num')
        sub = tracker.get_slot('subject')
        topic = tracker.get_slot('topic')
       
        print(sub_num)
        print(sub)
        print(topic)
      
        query = q.material_topic_in_course(sub,sub_num,topic)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            material_uri = [result['Course_Content_URI']['value'] for result in response.json()['results']['bindings']]
            material_name = [result['Material_Name']['value'] for result in response.json()['results']['bindings']]
            material_type = [result['Material_Type']['value'] for result in response.json()['results']['bindings']]
            formatted_materials = []

            for i in range(len(material_uri)):
                formatted_materials.append(f"{i+1}. {material_name[i]} ({material_type[i]}), {material_uri[i]}")

            # Join the formatted strings into a single string
            formatted_string = '\n'.join(formatted_materials)
            if formatted_string:
                # material_list = "\n".join(material)
                dispatcher.utter_message(text=f"Here are the materials covered in {sub} {sub_num} :\n{formatted_string}")
            else:
                dispatcher.utter_message(text=f"No material found for {sub} {sub_num}.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query6
class CreditsOfCourse(Action):

    def name(self):
        return "credits_of_course"

    def run(self, dispatcher, tracker, domain):
        sub_num = tracker.get_slot('sub_num')
        sub = tracker.get_slot('subject')
       
       
        print(sub_num)
        print(sub)
      
      
        query = q.credits_of_course(sub,sub_num)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            credits = [result['Credits']['value'] for result in response.json()['results']['bindings']]
            if credits:
                # material_list = "\n".join(material)
                dispatcher.utter_message(text=f"{sub} {sub_num} is a {credits[0]} credit course.")
            else:
                dispatcher.utter_message(text=f"No credits found for {sub} {sub_num}.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")
    
#Query7
class LinksCourseNumber(Action):

    def name(self):
        return "links_course_number"

    def run(self, dispatcher, tracker, domain):
        sub_num = tracker.get_slot('sub_num')
        sub = tracker.get_slot('subject')
       
       
        print(sub_num)
        print(sub)
      
      
        query = q.links_course_number(sub,sub_num)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            link = [result['Resource']['value'] for result in response.json()['results']['bindings']]
            if credits:
                # material_list = "\n".join(material)
                dispatcher.utter_message(text=f"You can refer to {link[0]} for more information on {sub} {sub_num}.")
            else:
                dispatcher.utter_message(text=f"No credits found for {sub} {sub_num}.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query8
class ContentOfLecInCourse(Action):

    def name(self):
        return "content_of_lec_in_course"

    def run(self, dispatcher, tracker, domain):
        sub_num = tracker.get_slot('sub_num')
        sub = tracker.get_slot('subject')
        lec = tracker.get_slot('lecture')
       
       
        print(sub_num)
        print(sub)
        print(lec)
      
      
        query = q.content_of_lec_in_course(sub,sub_num,lec)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            content_type = [result['Course_Content_URI']['value'] for result in response.json()['results']['bindings']]
            content_name = [result['Course_Content_Name']['value'] for result in response.json()['results']['bindings']]
            content_label = [result['Course_Content_Type_Label']['value'] for result in response.json()['results']['bindings']]
            
            formatted_content = []

            for i in range(len(content_type)):
                formatted_content.append(f"{i+1}. {content_name[i]} ({content_label[i]}), {content_type[i]}")

            # Join the formatted strings into a single string
            formatted_string = '\n'.join(formatted_content)
            
            if formatted_string:
                # content_list = "\n".join(content)
                dispatcher.utter_message(text=f"Here is a list of content for {sub} {sub_num} lecture {lec}:\n{formatted_string}")
            else:
                dispatcher.utter_message(text=f"No content found for lecture {lec} of {sub} {sub_num}.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query9
class ReadingForTopicCourse(Action):

    def name(self):
        return "reading_for_topic_course"

    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot('topic')
        course = tracker.get_slot('course')

        print(topic)
        print(course)
      
        query = q.reading_for_topic_course(topic,course)
        
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
                dispatcher.utter_message(text=f"Here is a list of readings for {course} :\n{formatted_string}")
            else:
                dispatcher.utter_message(text=f"No content found for readings found for {course}.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query10
class CompetencyByCourse(Action):

    def name(self):
        return "competency_by_course"

    def run(self, dispatcher, tracker, domain):
        sub_num = tracker.get_slot('sub_num')
        sub = tracker.get_slot('subject')

        print(sub_num)
        print(sub)
      
        query = q.competency_by_course(sub,sub_num)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            competency = [result['Topic_Name']['value'] for result in response.json()['results']['bindings']]
            if competency:
                competency_list = ",".join(competency)
                dispatcher.utter_message(text=f"On completing {sub} {sub_num} a student is competent in {competency_list}")
            else:
                dispatcher.utter_message(text=f"No competencies found for {sub} {sub_num} .")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query11
class StudentGradeInCourse(Action):

    def name(self):
        return "student_grade_in_course"

    def run(self, dispatcher, tracker, domain):
        fname = tracker.get_slot('fname')
        lname = tracker.get_slot('lname')
        sub_num = tracker.get_slot('sub_num')
        sub = tracker.get_slot('subject')

        print(sub_num)
        print(sub)
        print(fname)
        print(lname)
      
        query = q.student_grade_in_course(fname,lname,sub,sub_num)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            grade = [result['Grade']['value'] for result in response.json()['results']['bindings']]
            if grade:
                # competency_list = ",".join(competency)
                dispatcher.utter_message(text=f"{fname} {lname} has achieved {grade[0]} in {sub} {sub_num}")
            else:
                dispatcher.utter_message(text=f"No grade found for {fname} {lname} in {sub} {sub_num} .")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query12
class StudentCompletedCourses(Action):

    def name(self):
        return "student_completed_courses"

    def run(self, dispatcher, tracker, domain):
        
        # fname = tracker.get_slot('fname')
        # lname = tracker.get_slot('lname')
        sub_num = tracker.get_slot('sub_num')
        sub = tracker.get_slot('subject')

        print(sub_num)
        print(sub)
      
        query = q.student_completed_courses(sub,sub_num)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            students = [result['Student_Name']['value'] for result in response.json()['results']['bindings']]

            students_list = ''

            if students:
                for i, student in enumerate(students, 1):
                    students_list += f"{i}. {student}\n"
                dispatcher.utter_message(text=f"This is the list of students who have completed {sub} {sub_num} :\n{students_list}")
            else:
                dispatcher.utter_message(text=f"No students found for {sub} {sub_num}.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query13
class PrintTranscript(Action):

    def name(self):
        return "print_transcript"

    def run(self, dispatcher, tracker, domain):
        
        fname = tracker.get_slot('fname')
        lname = tracker.get_slot('lname')
        # sub_num = tracker.get_slot('sub_num')
        # sub = tracker.get_slot('subject')

        print(fname)
        print(lname)
      
        query = q.print_transcript(fname,lname)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        
        if response.status_code == 200:
            results = response.json()['results']['bindings']
            
            if results:
                students_list = []
                for result in results:
                    student_name = result['Student']['value']
                    course_name = result['Course_Name']['value']
                    grade = result['Grade']['value']
                    retake_grade = result.get('Retake_Grade', {}).get('value', '')  
                    students_list.append([student_name, course_name, grade, retake_grade])

                df = pd.DataFrame(students_list, columns=["Student Name", "Course Name", "Grade", "Retake Grade"])

                table_str = tabulate(df, headers="keys", tablefmt="pipe", showindex=False)
               
                dispatcher.utter_message(text=f"Here is {fname} {lname}'s transcript:\n{table_str}")
            else:
                dispatcher.utter_message(text=f"No transcript found for {fname} {lname}.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query14
class TotalTriples(Action):

    def name(self):
        return "total_triples"

    def run(self, dispatcher, tracker, domain):
        
        # fname = tracker.get_slot('fname')
        # lname = tracker.get_slot('lname')
        # sub_num = tracker.get_slot('sub_num')
        # sub = tracker.get_slot('subject')

        # print(sub_num)
        # print(sub)
      
        query = q.total_triples()
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            triples = [result['Total_Number_of_Triples']['value'] for result in response.json()['results']['bindings']]
            if triples:
                # students_list = ",".join(students)
                dispatcher.utter_message(text=f"I am made up of {triples[0]} triples.")
            else:
                dispatcher.utter_message(text=f"I have no triples in me.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query15
class NumOfCourses(Action):

    def name(self):
        return "num_of_courses"

    def run(self, dispatcher, tracker, domain):
        
        # fname = tracker.get_slot('fname')
        # lname = tracker.get_slot('lname')
        # sub_num = tracker.get_slot('sub_num')
        # sub = tracker.get_slot('subject')

        # print(sub_num)
        # print(sub)
      
        query = q.num_of_courses()
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            c_count = [result['Course_Count']['value'] for result in response.json()['results']['bindings']]
            if c_count:
                # students_list = ",".join(students)
                dispatcher.utter_message(text=f"I have {c_count[0]} courses in me.")
            else:
                dispatcher.utter_message(text=f"I have no courses in me.")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")
#Query16
class CourseNumber(Action):

    def name(self):
        return "course_number"

    def run(self, dispatcher, tracker, domain):
        
        # fname = tracker.get_slot('fname')
        # lname = tracker.get_slot('lname')
        sub_num = tracker.get_slot('sub_num')
        sub = tracker.get_slot('subject')

        print(sub_num)
        print(sub)
      
        query = q.course_number(sub,sub_num)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            c_des = [result['Course_Description']['value'] for result in response.json()['results']['bindings']]
            if c_des:
                # students_list = ",".join(students)
                dispatcher.utter_message(text=f"\n{c_des[0]}\n")
            else:
                dispatcher.utter_message(text=f"No description found for {sub} {sub_num}")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")
#Query17
class TopicsCourseEventCourse(Action):

    def name(self):
        return "topics_course_event_course"

    def run(self, dispatcher, tracker, domain):
        
        # fname = tracker.get_slot('fname')
        # lname = tracker.get_slot('lname')
        sub_num = tracker.get_slot('sub_num')
        sub = tracker.get_slot('subject')
        evt = tracker.get_slot('event')
        event_num = tracker.get_slot('event_num')

        print(sub_num)
        print(sub)
        print(evt)
        print(event_num)
      
        query = q.topics_course_event_course(sub,sub_num,evt,event_num)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            topics = [result['Topic_Name']['value'] for result in response.json()['results']['bindings']]
            if topics:
                topics_list = ",".join(topics)
                dispatcher.utter_message(text=f"{topics_list} are the topics covered in {evt} {event_num} of {sub} {sub_num}")
            else:
                dispatcher.utter_message(text=f"No are the topics covered in {evt} {event_num} of {sub} {sub_num}")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

#Query18
class TopicsInCourseEvents(Action):

    def name(self):
        return "topics_in_course_events"

    def run(self, dispatcher, tracker, domain):
        
        # fname = tracker.get_slot('fname')
        # lname = tracker.get_slot('lname')
        # sub_num = tracker.get_slot('sub_num')
        # sub = tracker.get_slot('subject')
        # evt = tracker.get_slot('event')
        # lec_num = tracker.get_slot('lecture')
        topic = tracker.get_slot('topic')

        # print(sub_num)
        # print(sub)
        # print(evt)
        print(topic)
      
        query = q.topics_in_course_events(topic)
        
        response = requests.post('http://localhost:3030/Graph/query', data={'query': query})
        if response.status_code == 200:
           
            event = [result['Course_Event']['value'] for result in response.json()['results']['bindings']]
            course = [result['Course_Name']['value'] for result in response.json()['results']['bindings']]
            formatted_content = []

            for i in range(len(course)):
                formatted_content.append(f"{i+1}. {event[i]} of {course[i]}.")

            formatted_string = '\n'.join(formatted_content)
            if formatted_string:
                # event_list = ",".join(event)
                dispatcher.utter_message(text=f"The topic {topic} is covered by: \n{formatted_string}")
            else:
                dispatcher.utter_message(text=f"No course covers the topic {topic}")
        else:
            dispatcher.utter_message(text="Failed to fetch information from the database.")

class FallbackAction(Action):
    def name(self) -> Text:
        return "action_default_fallback"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("I'm sorry, I couldn't understand your question. ")
        dispatcher.utter_message("Here are some suggestions:")
        dispatcher.utter_message("- Please try rephrasing your question.")
        dispatcher.utter_message("- You can also try asking a different question.")


