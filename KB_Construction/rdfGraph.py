import pandas as pd
import numpy as np
from rdflib import Graph, Namespace, URIRef, Literal,RDF,RDFS,FOAF,XSD
from urllib.parse import quote
from datacleaning import preProcessData
from entitytag import getTopics
import math
import os

roboprof = Namespace("http://roboprof.ca/schema/")
roboprof_data = Namespace("http://roboprof.ca/data/")
dbp = Namespace("http://dbpedia.org/property/")
dbo = Namespace("http://dbpedia.org/ontology/")
dbr = Namespace("http://dbpedia.org/resources/")
# rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema/")
# rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns/")
dce = Namespace("http://purl.org/dc/elements/1.1/")
vivo = Namespace("http://vivoweb.org/ontology/core/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
# xsd = Namespace("http://www.w3.org/2001/XMLSchema")
schema = Namespace("http://schema.org/")
dcterms = Namespace("http://purl.org/dc/terms/")
wd = Namespace("http://www.wikidata.org/entity/")
vcard = Namespace("https://www.w3.org/2006/vcard/ns/")
concordia_uri = roboprof_data.ConcordiaUniversity
parent_directory = os.path.dirname(os.getcwd())



def buildGraph():

    g = Graph()

    g.bind("dbp", dbp)
    g.bind("dbo", dbo)
    g.bind("dbr", dbr)
    # g.bind("rdfs", rdfs)
    # g.bind("rdf", rdf)
    # g.bind("rdfs", rdfs)
    # g.bind("rdf", rdf)
    g.bind("dce", dce)
    g.bind("vivo", vivo)
    # g.bind("foaf", foaf)
    # g.bind("xsd", xsd)
    g.bind("schema", schema)
    g.bind("dcterms", dcterms)
    g.bind("wd", wd)
    g.bind("vcard", vcard)
    g.bind("roboprof", roboprof)
    g.bind("roboprof_data", roboprof_data)

    # parent_directory = os.path.dirname(os.getcwd())

    # print(parent_directory)

    # g.parse(r".\dataset\vocabulary.rdf",format='turtle')

    g.parse(parent_directory+"\\RDF Schema\\vocabulary.ttl",format='turtle')

    #build a university graph
    g = buildUniversityGraph(g)

    #build a course graph
    g = buildCoursesGraph(g)

    #build a lectures graph
    g = buildLecturesAndTopicsGraph(g)

    #build a topics graph
    g = buildLabsAndTopicsGraph(g)

    #build a students graph
    g = buildStudentsGraph(g)

    # create ttl file
    output_file_path = parent_directory+"\\Knowledge Base\\"+"Graph.ttl"
    g.serialize(destination=output_file_path, format="turtle")

    output_file_path_nt = parent_directory+"\\Knowledge Base\\"+"Graph.nt"
    g.serialize(destination=output_file_path_nt, format="nt",encoding="utf-8")

    return 0

def buildUniversityGraph(g):

    # concordia_uri = roboprof_data.ConcordiaUniversity
    g.add((concordia_uri, RDF.type, dbo.University))
    g.add((concordia_uri,dbo.name, Literal("Concordia University")))
    g.add((concordia_uri,RDFS.seeAlso, URIRef("https://dbpedia.org/resource/Concordia_University")))

    return g

def buildCoursesGraph(g):

    # print("Function Called")

    df = preProcessData()

    # print(len(df))
   
    for index, row in df.iterrows():

        # print(int(row["Number"]))
        course_code = str(row["Subject"]+"_"+str(int(row["Number"]))).replace(" ","")
        course_uri = roboprof_data[course_code] 

        g.add((course_uri, RDF.type, vivo.Course))
        g.add((course_uri,dbo.name,Literal(row["Name"])))
        g.add((course_uri,vivo.hasSubjectArea,Literal(row["Subject"])))
        g.add((course_uri,dbo.number,Literal(int(row["Number"]))))
        g.add((course_uri,vivo.courseCredits,Literal(row["Credits"])))
        g.add((course_uri,dcterms.description,Literal(row["Description"])))
        if not pd.isna(row['Link']):
            g.add((course_uri,RDFS.seeAlso,URIRef(row["Link"])))
        if not pd.isna(row['Outline']):
            g.add((course_uri,roboprof.courseOutline,URIRef(row["Outline"])))
        g.add((concordia_uri,roboprof.offersCourse,course_uri))

        if not pd.isna(row['CourseEvent']):
        
            lst_event = row["CourseEvent"].split(",")
            # print(lst_lectures)

            for evt in lst_event:
                # print(lec)
                evt_uri = roboprof_data[str(course_code+"_"+evt).replace(" ","_")]
                # print(lec_uri)
                # lec_uri = roboprof_data[lec.replace(" ","_")] 
                g.add((course_uri,roboprof.hasCourseEvent,evt_uri))

    return g

def buildLabsAndTopicsGraph(g):

    df = pd.read_excel(parent_directory+"\\Datasets\\dataset.xlsx",sheet_name="Labs")

    # print(df)

    # i = 0

    for index, row in df.iterrows():

        # i = i+1
        # print(i)cls

        directory = parent_directory + '/Datasets/Lab Content/'+row['Course']+'/Lab Material/'
        

        lab_uri = roboprof_data[str(row["Course"]+"_Lab_"+str(int(row["Number"]))).replace(" ","_")] 
     
        g.add((lab_uri,RDF.type,roboprof.Lab))
        g.add((lab_uri,dbo.number,Literal(int(row["Number"]))))
        g.add((lab_uri,dbo.name,Literal(row["Name"])))

        mat_uri = quote(row["Material"], safe=':/')
        mat_uri = URIRef(mat_uri)
        g.add((mat_uri,RDF.type,roboprof.LabMaterial))
        g.add((lab_uri,roboprof.coversCourseContent ,mat_uri))
        # print(str(lab_uri)+" : "+str(mat_uri))
        lab_name = row["Material"].split("/")[-1]
        g.add((mat_uri,dbo.name ,Literal(lab_name)))
        lab_file = lab_name.split(".")[0]+".txt"
        g = addTopicsGraph(g,lab_file,mat_uri,directory)

    return g

def buildLecturesAndTopicsGraph(g):

    df = pd.read_excel(parent_directory+"\\Datasets\\dataset.xlsx",sheet_name="Lectures")

    # print(df.columns)

    for index, row in df.iterrows():

        
        

        lec_uri = roboprof_data[str(row["Course"]+"_Lecture_"+str(int(row["Number"]))).replace(" ","_")] 
     
        g.add((lec_uri,RDF.type,roboprof.Lecture))
        g.add((lec_uri,dbo.number,Literal(int(row["Number"]))))
        g.add((lec_uri,dbo.name,Literal(row["Name"])))

        # Adding Slide Info
        directory = parent_directory + '/Datasets/Lecture Content/'+row['Course']+'/Lectures/'
        slide_uri = quote(row["Slides"], safe=':/')
        slide_uri = URIRef(slide_uri)
        g.add((slide_uri,RDF.type,roboprof.Slide))
        g.add((lec_uri,roboprof.coversCourseContent ,slide_uri))
        slide_name = row["Slides"].split("/")[-1]
        g.add((slide_uri,dbo.name ,Literal(slide_name)))
        slide_file = slide_name.split(".")[0]+".txt"
        g = addTopicsGraph(g,slide_file,slide_uri,directory)

        # Adding Worksheet Info
        directory = parent_directory + '/Datasets/Lecture Content/'+row['Course']+'/Worksheets/'
        worksheet_uri = quote(row["Worksheet"], safe=':/')
        worksheet_uri = URIRef(worksheet_uri)
        g.add((worksheet_uri,RDF.type,roboprof.Worksheet))
        g.add((lec_uri,roboprof.coversCourseContent ,worksheet_uri))
        worksheet_name = row["Worksheet"].split("/")[-1]
        g.add((worksheet_uri,dbo.name ,Literal(worksheet_name)))
        worksheet_file = worksheet_name.split(".")[0]+".txt"
        g = addTopicsGraph(g,worksheet_file,worksheet_uri,directory)

        # Adding Reading Info
        if not pd.isna(row['Reading']):
            directory = parent_directory + '/Datasets/Lecture Content/'+row['Course']+'/Readings/'
            reading_uri = quote(row["Reading"], safe=':/')
            reading_uri = URIRef(reading_uri)
            g.add((reading_uri,RDF.type,roboprof.Reading))
            g.add((lec_uri,roboprof.coversCourseContent ,reading_uri))
            reading_name = row["Reading"].split("/")[-1]
            g.add((reading_uri,dbo.name ,Literal(reading_name)))
            reading_file = reading_name.split(".")[0]+".txt"
            g = addTopicsGraph(g,reading_file,reading_uri,directory)

        # Adding Other Material Info
        if not pd.isna(row['Others']):
            directory = parent_directory + '/Datasets/Lecture Content/'+row['Course']+'/OtherMaterial/'
            others_uri = quote(row["Others"], safe=':/')
            others_uri = URIRef(others_uri)
            g.add((others_uri,RDF.type,roboprof.OtherMaterial))
            g.add((lec_uri,roboprof.coversCourseContent ,others_uri))
            others_name = row["Others"].split("/")[-1]
            g.add((others_uri,dbo.name ,Literal(others_name)))
            others_file = others_name.split(".")[0]+".txt"
            g = addTopicsGraph(g,others_file,others_uri,directory)

        #Adding Links
        if not pd.isna(row['Link']):
            g.add((lec_uri,RDFS.seeAlso,URIRef(row["Link"])))


        
        

        # topic_df = getTopics(file)

        # for index_t, row_t in topic_df.iterrows():
        #     topic_uri = URIRef(row_t['uri'])
        #     topic_name = row_t['name']
        #     g.add((topic_uri,RDF.type,roboprof.Topic))
        #     g.add((topic_uri,dbo.name,Literal(topic_name)))
        #     g.add((topic_uri,roboprof.provenanceInfo,slide_uri))




    return g


def addTopicsGraph(g,filename,content_uri,directory):

    file = directory + 'text_files/'+filename
    topic_df = getTopics(file)

    for index_t, row_t in topic_df.iterrows():
        topic_uri = URIRef(row_t['uri'])
        topic_name = row_t['name']
        if(topic_name == 'Aloha'):
            print(topic_uri)
        g.add((topic_uri,RDF.type,roboprof.Topic))
        g.add((topic_uri,dbo.name,Literal(topic_name)))
        g.add((topic_uri,roboprof.provenanceInfo,content_uri))


    return g



def buildStudentsGraph(g):

    df = pd.read_excel(parent_directory+"\\Datasets\\dataset.xlsx",sheet_name="Students")

    for index, row in df.iterrows():

        student_uri = roboprof_data[str(row["ID"])]
      
        g.add((student_uri,RDF.type,vivo.Student))
        g.add((student_uri,FOAF.firstName,Literal(row["First Name"].replace(" ",""))))
        g.add((student_uri,FOAF.lastName,Literal(row["Last Name"].replace(" ",""))))
        g.add((student_uri,vcard.hasEmail,Literal(row["Email"])))
        course_uri = roboprof_data[str(row["Completed Courses"]).replace(" ","_")]
        g.add((student_uri,roboprof.completedCourse,course_uri))
        g.add((student_uri,roboprof.studiesAt,concordia_uri))

        grade = str(row["Completed Courses"]+" "+row["Initial Grade"]).replace(" ","_")
        grade_uri = roboprof_data[grade]
        

        g.add((grade_uri,RDF.type,roboprof.InitialGrade))

        g.add((grade_uri,roboprof.gradeValue,Literal(row["Initial Grade"].strip())))
        
        g.add((student_uri,roboprof.achievedGrade,grade_uri))

        g.add((grade_uri,roboprof.gradeInCourse,course_uri))

        if row["isRetake"] == 1:

            grade_re = "Retake/"+str(row["Completed Courses"]+" "+row["Final Grade"]).replace(" ","_")
            grade_uri_re = roboprof_data[grade_re]
          
            g.add((grade_uri_re,RDF.type,roboprof.RetakeGrade))

            g.add((grade_uri_re,roboprof.gradeValue,Literal(row["Final Grade"].strip())))
            
            g.add((student_uri,roboprof.achievedGrade,grade_uri_re))

            g.add((grade_uri_re,roboprof.gradeInCourse,course_uri))


        


    return g



