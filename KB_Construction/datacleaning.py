import pandas as pd
import numpy as np
import os

def preProcessData():

    parent_directory = os.path.dirname(os.getcwd())

    concordiaCatalog = pd.read_excel(parent_directory+"\\Datasets\\dataset.xlsx",sheet_name="Courses")
    df = concordiaCatalog.copy()
   
    temp = df[df["Subject"].notnull()].copy()
   
    df = temp
    temp = df[df["Number"].notnull()].copy()
    
    df = temp.copy()

    df = df.drop_duplicates()
    
    
    return df
