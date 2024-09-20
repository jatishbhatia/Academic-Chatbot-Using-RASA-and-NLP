prefix = '''
            PREFIX dbp: <http://dbpedia.org/property/>
            PREFIX db: <http://dbpedia.org/>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX roboprof: <http://roboprof.ca/schema/>
            PREFIX roboprof_data: <http://roboprof.ca/data/>
            PREFIX vivo: <http://vivoweb.org/ontology/core/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            
        '''
#Query1
def courses_by_uni(uni_name):

    q = prefix + '''SELECT ?University ?Course_Name ?Course_URI
            WHERE {{
                ?uni dbo:name "{}" .
                ?uni dbo:name ?University .
                ?uni roboprof:offersCourse ?Course_URI .
                ?Course_URI dbo:name ?Course_Name .
            }}
     '''.format(uni_name)
    
    # print(q)

    
    return q

# print(courses_by_uni("Concordia University"))

#Query2
def course_discussed_topic(topic):
    
    q = prefix + '''SELECT DISTINCT ?Course_URI ?Course_Name ("{}" AS ?Topic_Name)
            WHERE {{
                ?Topic_URI dbo:name "{}" .
                ?Topic_URI roboprof:provenanceInfo ?Course_Content_URI .
                ?CourseEvent_URI roboprof:coversCourseContent ?Course_Content_URI .
                ?Course_URI roboprof:hasCourseEvent ?CourseEvent_URI .
                ?Course_URI dbo:name ?Course_Name .
            }}
        '''.format(topic,topic)
    
    return q

# print(course_discussed_topic("Deep Learning"))

#Query3
def topics_in_course_lec(course,lec):

    q = prefix + '''SELECT ?Topic_URI ?Topic_Name ("{}" AS ?Course_Name) (STR({}) AS ?Lecture_Number)
                WHERE {{
                    ?course dbo:name "{}" .
                    ?course roboprof:hasCourseEvent ?CourseEvent_URI .
                    ?CourseEvent_URI rdf:type ?CourseEvent_Type .
                    ?CourseEvent_Type rdfs:label "Lecture"@en .
                    ?CourseEvent_URI dbo:number {} .
                    ?CourseEvent_URI roboprof:coversCourseContent ?Course_Content_URI .
                    ?Topic_URI roboprof:provenanceInfo ?Course_Content_URI .
                    ?Topic_URI dbo:name ?Topic_Name .
                }}
        '''.format(course,lec,course,lec)
    
    return q

# print(topics_in_course_lec("Deep Learning","Intelligent Systems"))

#Query4
def courses_by_uni_subject(uni,sub):

    q = prefix + '''SELECT ?Course_URI ?Course_Name ("{}" AS ?University_Name) ("{}" AS ?Subject)
                WHERE {{
                    ?uni dbo:name "{}" .
                    ?Course_URI dbo:name ?Course_Name .
                    ?uni roboprof:offersCourse ?Course_URI .
                    ?Course_URI vivo:hasSubjectArea "{}" .
                }}
        '''.format(uni,sub,uni,sub)
    
    return q

# print(courses_by_uni_subject("Concordia University","COMP"))

#Query5
def material_topic_in_course(subject,number,topic):

    q = prefix + '''SELECT DISTINCT ?Course_Name (CONCAT("{}", " ", STR({})) AS ?Course_Number) ("{}" AS ?Topic_Name) ?Course_Content_URI ?Material_Type ?Material_Name
                WHERE {{
                    ?course dbo:number {} .
                    ?course vivo:hasSubjectArea "{}" .
                    ?course dbo:name ?Course_Name .
                    ?course roboprof:hasCourseEvent ?CourseEvent_URI .
                    ?Topic_URI dbo:name "{}" .
                    ?CourseEvent_URI roboprof:coversCourseContent ?Course_Content_URI .
                    ?Course_Content_URI dbo:name ?Material_Name .
                    ?Course_Content_URI rdf:type ?Course_Content_Type .
                    ?Course_Content_Type rdfs:label ?Material_Type .
                }}
        '''.format(subject,number,topic,number,subject,topic)
    
    return q

# print(material_topic_in_course("COMP","6741","Deep Learning"))

#Query6
def credits_of_course(subject,number):

    q = prefix + '''SELECT ?Course_Name (CONCAT("{}", " ", STR({})) AS ?Course_Number) ?Credits
                WHERE {{
                    ?course dbo:number {} .
                    ?course vivo:hasSubjectArea "{}" .
                    ?course dbo:name ?Course_Name .
                    ?course vivo:courseCredits ?Credits .
                }}
        '''.format(subject,number,number,subject)
    
    return q

# print(credits_of_course("COMP","6741"))

#Query7
def links_course_number(subject,number):

    q = prefix + '''SELECT ?Course_Name (CONCAT("{}", " ", STR({})) AS ?Course_Number) ?Resource
                    WHERE {{
                        ?course dbo:number {} .
                        ?course vivo:hasSubjectArea "{}" .
                        ?course dbo:name ?Course_Name .
                        ?course rdfs:seeAlso ?Resource .
                    }}
        '''.format(subject,number,number,subject)
    
    return q
#Query8
def content_of_lec_in_course(subject,number,lec):

    q = prefix + '''SELECT ?Course_Name (CONCAT("{}", " ", STR({})) AS ?Course_Number) (STR({}) AS ?Lecture_Number) ?Course_Content_URI ?Course_Content_Type_Label ?Course_Content_Name
                    WHERE {{
                        ?course dbo:number {} .
                        ?course vivo:hasSubjectArea "{}" .
                        ?course dbo:name ?Course_Name .
                        ?course roboprof:hasCourseEvent ?CourseEvent_URI .
                        ?CourseEvent_URI rdf:type ?CourseEvent_Type .
                        ?CourseEvent_Type rdfs:label "Lecture"@en .
                        ?CourseEvent_URI dbo:number {} .
                        ?CourseEvent_URI roboprof:coversCourseContent ?Course_Content_URI .
                        ?Course_Content_URI dbo:name ?Course_Content_Name .
                        ?Course_Content_URI rdf:type ?Course_Content_Type .
                        ?Course_Content_Type rdfs:label ?Course_Content_Type_Label .
                    }}
        '''.format(subject,number,lec,number,subject,lec)
    
    return q
#Query9
def reading_for_topic_course(topic,course):

    q = prefix + '''SELECT DISTINCT ("{}" AS ?Course_Name) ("{}" AS ?Topic_Name) ?Course_Content_URI ?Course_Content_Type_Label ?Course_Content_Name
                WHERE {{
                    ?course dbo:name "{}" .
                    ?course roboprof:hasCourseEvent ?CourseEvent_URI .
                    ?CourseEvent_URI roboprof:coversCourseContent ?Course_Content_URI .
                    ?Course_Content_URI rdf:type roboprof:Reading .
                    ?Topic_URI dbo:name "{}" .
                    ?Topic_URI roboprof:provenanceInfo ?Course_Content_URI .
                    ?Course_Content_URI dbo:name ?Course_Content_Name .
                    ?Course_Content_URI rdf:type ?Course_Content_Type .
                    ?Course_Content_Type rdfs:label ?Course_Content_Type_Label .
                }}
        '''.format(course,topic,course,topic)
    
    return q
#Query10
def competency_by_course(sub,number):

    q = prefix + '''SELECT DISTINCT ?Course_Name (CONCAT("{}", " ", STR({})) AS ?Course_Number) ?Topic_Name ?Topic_URI
                    WHERE {{
                        ?course dbo:number {} .
                        ?course vivo:hasSubjectArea "{}" .
                        ?course dbo:name ?Course_Name .
                        ?course roboprof:hasCourseEvent ?CourseEvent_URI .
                        ?CourseEvent_URI roboprof:coversCourseContent ?Course_Content_URI .
                        ?Topic_URI roboprof:provenanceInfo ?Course_Content_URI .
                        ?Topic_URI dbo:name ?Topic_Name .
                    }}
        '''.format(sub,number,number,sub)
    
    return q
#Query11
def student_grade_in_course(fname,lname,subject,number):

    q = prefix + '''SELECT (CONCAT("{}", " ", "{}") AS ?Name) ?Course_Name (CONCAT("{}", " ", STR({})) AS ?Course_Number) ?Grade ?Grade_URI
                    WHERE {{
                        ?student foaf:firstName "{}" .
                        ?student foaf:lastName "{}" .
                        ?student roboprof:achievedGrade ?Grade_URI .
                        ?course dbo:number {} .
                        ?course vivo:hasSubjectArea "{}" .
                        ?course dbo:name ?Course_Name .
                        ?Grade_URI roboprof:gradeInCourse ?course .
                        ?Grade_URI roboprof:gradeValue ?Grade .
                    }}
        '''.format(fname,lname,subject,number,fname,lname,number,subject)
    
    return q
#Query12
def student_completed_courses(subject,number):

    q = prefix + '''SELECT DISTINCT (CONCAT("{}", " ", STR({})) AS ?Course_Number) (CONCAT(?first_name, " ", ?last_name) AS ?Student_Name) ?Student_URI
                    WHERE {{
                        ?course dbo:number {} .
                        ?course vivo:hasSubjectArea "{}" .
                        ?Student_URI roboprof:completedCourse ?course .
                        ?course dbo:name ?course_name .
                        ?Student_URI foaf:firstName ?first_name .
                        ?Student_URI foaf:lastName ?last_name .
                    }}
        '''.format(subject,number,number,subject)
    
    return q
#Query13
def print_transcript(fname,lname):

    q = prefix + '''SELECT (CONCAT("{}", " ", "{}") AS ?Student) ?Course_Name ?Course_URI ?Grade ?Grade_URI ?Retake_Grade ?Retake_Grade_URI
                WHERE {{
                    ?student foaf:firstName "{}" .
                    ?student foaf:lastName "{}" .
                    ?student roboprof:completedCourse ?Course_URI .
                    ?Course_URI dbo:name ?Course_Name .
                    ?student roboprof:achievedGrade ?Grade_URI .
                    ?Grade_URI rdf:type roboprof:InitialGrade .
                    ?Grade_URI roboprof:gradeInCourse ?Course_URI .
                    ?Grade_URI roboprof:gradeValue ?Grade .
                    OPTIONAL {{ ?student roboprof:achievedGrade ?Retake_Grade_URI .
                            ?Retake_Grade_URI rdf:type roboprof:RetakeGrade .
                            ?Retake_Grade_URI roboprof:gradeInCourse ?Course_URI .
                            ?Retake_Grade_URI roboprof:gradeValue ?Retake_Grade . }}    
                }}

        '''.format(fname,lname,fname,lname)
    
    return q
#Query14
def total_triples():

    q = prefix + '''SELECT (COUNT(?s) AS ?Total_Number_of_Triples)
                WHERE {{
                    ?s ?p ?o .
                }}
                '''
    
    return q
#Query15
def num_of_courses():

    q = prefix + '''SELECT (COUNT(?courses) AS ?Course_Count)
                    WHERE {{
                    ?courses rdf:type vivo:Course .
                    }}
                    '''
    
    return q
#Query16
def course_number(subject,number):

    q = prefix +'''SELECT ?Course_Name (CONCAT("{}", " ", STR({})) AS ?Course_Number) ?Course_Description
                WHERE {{
                    ?course dbo:number {} .
                    ?course vivo:hasSubjectArea "{}" .
                    ?course dbo:name ?Course_Name .
                    ?course dcterms:description ?Course_Description .
                }}'''.format(subject,number,number,subject)


    return q
#Query17
def topics_course_event_course(subject,number,evt,lec):

    q = prefix +'''SELECT ?Topic_URI ?Topic_Name (CONCAT("{}", " ", STR({})) AS ?Course_Number) (CONCAT("{}", " ", STR({})) AS ?CourseEvent)
                WHERE {{
                    ?course dbo:number {} .
                    ?course vivo:hasSubjectArea "{}" .
                    ?course roboprof:hasCourseEvent ?CourseEvent_URI .
                    ?CourseEvent_URI rdf:type ?CourseEvent_Type .
                    ?CourseEvent_Type rdfs:label "{}"@en .
                    ?CourseEvent_URI dbo:number {} .
                    ?CourseEvent_URI roboprof:coversCourseContent ?Course_Content_URI .
                    ?Topic_URI roboprof:provenanceInfo ?Course_Content_URI .
                    ?Topic_URI dbo:name ?Topic_Name .
                }}'''.format(subject,number,evt,lec,number,subject,evt,lec)
                    
    return q
#Query18
def topics_in_course_events(topic):

    q = prefix +'''SELECT DISTINCT ("{}" AS ?Topic_Name) (COUNT(?Topic_URI) AS ?Frequency) ?Course_Name ?Course_URI (CONCAT(?CourseEvent_Type_Label, " ", STR(?CourseEvent_Num)) AS ?Course_Event) ?CourseEvent_URI ?CourseEvent_Type
                    WHERE {{
                        ?Topic_URI dbo:name "{}" .
                        ?Topic_URI roboprof:provenanceInfo ?Course_Content_URI .
                        ?CourseEvent_URI roboprof:coversCourseContent ?Course_Content_URI .
                        ?CourseEvent_URI rdf:type ?CourseEvent_Type .
                        ?CourseEvent_Type rdfs:label ?CourseEvent_Type_Label .
                        ?CourseEvent_URI dbo:number ?CourseEvent_Num .
                        ?Course_URI roboprof:hasCourseEvent ?CourseEvent_URI .
                        ?Course_URI dbo:name ?Course_Name .
                    }}
                    GROUP BY ?Topic_Name ?Frequency ?Course_Name ?Course_URI ?CourseEvent_Type_Label ?CourseEvent_URI ?CourseEvent_Type ?CourseEvent_Num
                    ORDER BY DESC(?Frequency)
                '''.format(topic,topic)
                    
    return q

