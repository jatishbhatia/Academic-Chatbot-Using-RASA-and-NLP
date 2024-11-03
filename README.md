# This project contains the following files/folders - 

1. RDF Schema: The RDFS file in Turtle format called vocabulary.ttl

2. Dataset: The dataset used to construct the knowledge base
   This directory contains the following files/folders -  
   2.1. Lecture Content : The material for the two courses into suitable datasets  
   2.2. CATALOG : Information about Concordia's courses from the open datasets available at https://opendata.concordia.ca/datasets/  
   2.3 dataset : This excel file ontains different sheets containing the entire dataset used to populate the Knowledge Base. It includes the open data as well the manually created triples, everything according to the schema.   
   2.4 Vocab_info : Roughly states the Classes/Properties used according to the required model as per the project description.   

4. KB Construction: Python program files to automatically construct the knowledge base from the dataset
   This directory contains the following files -     
   3.1 main.py : Main file to run the program  
   3.2 datacleaning.py : For data pre-processing  
   3.3 rdfGraph.py : To build the knowledge base  

5. Knowledge Base: Complete constructed knowledge base in both N-Triples(Graph.nt) and Turtle(Graph.ttl) format

6. Queries and Results: Text files with the queries for the questions(q1.txt, q2.txt,..) and the full output of the queries when run on the KB using Apache Fuseki(q1-out.csv, q2-out.csv,..)

7. Report: The project report, as detailed PDF as detailed in the project description.

# Steps to execute the code : 

1. Install all the required libraries to run this project using the requirements.txt file. Switch directory to the location of this README file and run the below command.

   pip install -r requirements.txt

3. Switch your directory to "KB Construction" which contains the file main.py 

4. Run the main file by using the below command.

   python main.py

6. This will generate the knowledge base files located inside the Knowledge Base directory. The knowledge base will be created in two formats - N-Triples(Graph.nt) and Turtle(Graph.ttl)

7. Follow the steps to install the Apache Fuseki server as given in the report. 

8. Run the server and create a new dataset. Upload the generated knowledge base file "Graph.ttl"

9. Go to the Queries tab and run the queries given in the directory - Queries and Results to get the output.  

# Report
[View Report (PDF)](https://github.com/jatishbhatia/Chatbot-Using-RASA-and-NLP/blob/main/Report/Report.pdf)
The report has detailed explanation about the project.

# Some example chatbot outputs

![image](https://github.com/user-attachments/assets/0a95796d-a872-4bcb-99c9-8c07cc3f6894)
![image](https://github.com/user-attachments/assets/0a5f2b2e-b3b8-44a7-9796-452298166d16)
![image](https://github.com/user-attachments/assets/3ec43d6c-80c5-45b9-8801-1675e55e9f61)
![image](https://github.com/user-attachments/assets/e6bc4eca-1dae-4dbf-9237-07ac3bc447ed)

