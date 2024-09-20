import spacy_dbpedia_spotlight
import spacy
import os
import pandas as pd

parent_directory = os.path.dirname(os.getcwd())

def getTopics(file):

    nlp = spacy.load('en_core_web_sm')

    nlp.add_pipe('dbpedia_spotlight')

    content = ""
    with open(file, 'r',encoding='utf-8') as file:
    
        content = file.read()
   
    doc = nlp(content)
    names = []
    urls = []
    pos = []
    kb_scores = []

    for ent in doc.ents:
        
        if ent.kb_id_:
           
            if all(token.pos_ == 'PROPN' for token in ent) or (len(ent) >= 2 and ent[0].pos_ == 'VERB' and ent[1].pos_ == 'PROPN'):
                score = ent._.dbpedia_raw_result.get('@similarityScore', 0)
                if(float(score) == 1.0):
                    names.append(ent.text)
                    urls.append(ent.kb_id_)
                    pos.append([token.pos_ for token in ent])
                    kb_scores.append(ent._.dbpedia_raw_result['@similarityScore'])

            
    df = pd.DataFrame({'name': names, 'uri': urls,'score':kb_scores})

    existing_df = pd.read_excel(parent_directory+"\\Datasets\\Topics.xlsx")

    # updated_df = existing_df.append(df, ignore_index=True)

    updated_df = pd.concat([existing_df, df], ignore_index=True)


    updated_df = updated_df.drop_duplicates()

    updated_df.to_excel(parent_directory+"\\Datasets\\Topics.xlsx", index=False)


    return df


# parent_directory = os.path.dirname(os.getcwd())
# directory = parent_directory + '/Datasets/Lecture Content/COMP 6741/Lectures/'
# file = directory + 'text_files/slides01.txt'

# getTopics(file)

    # for ent in doc.ents:
    #     if ent.kb_id_:
    #         print(f"Entity: {ent.text}")
    #         print(f"DBpedia URL: http://dbpedia.org/resource/{ent.text.replace(' ', '_')}")
    #         print(f"DBpedia ID: {ent.kb_id_}")
    #         print(f"Similarity Score: {ent._.dbpedia_raw_result['@similarityScore']}")
    #         print(f'Entity Label: {ent.label_}')
    #         print("---------------")





# nlp = spacy.load('en_core_web_sm')

# nlp.add_pipe('dbpedia_spotlight')

# content = ''

# with open(file, 'r',encoding='utf-8') as file:
#     # Read the entire contents of the file
#     content = file.read()
#     # print(content)

# # doc = nlp('Google LLC is an American multinational technology company.')
# doc = nlp(content)

# for ent in doc.ents:
#     if ent.kb_id_:
#         print(f"Entity: {ent.text}")
#         print(f"DBpedia URL: http://dbpedia.org/resource/{ent.text.replace(' ', '_')}")
#         print(f"DBpedia ID: {ent.kb_id_}")
#         print(f"Similarity Score: {ent._.dbpedia_raw_result['@similarityScore']}")
#         print(f'Entity Label: {ent.label_}')
#         print("---------------")



# print([(ent.text, ent.kb_id_, ent._.dbpedia_raw_result['@similarityScore'],ent.label_) for ent in doc.ents])
