from pptx import Presentation
import win32com.client
import os
parent_directory = os.path.dirname(os.getcwd())

def ppt_to_text(ppt_file):

    ppt_app = win32com.client.Dispatch("PowerPoint.Application")
    presentation = ppt_app.Presentations.Open(ppt_file)
    
    text = ''
    for slide in presentation.Slides:
        for shape in slide.Shapes:
            if shape.HasTextFrame:
                text += shape.TextFrame.TextRange.Text + '\n'
    
    presentation.Close()
    ppt_app.Quit()
    
    return text.strip()


def main(directory):
    # directory = parent_directory + '/Datasets/Lecture Content/COMP 6461/Lectures/'
    text_folder = directory + 'text_files/'
    
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)
    

    for filename in os.listdir(directory):
        if filename.endswith(".ppt") or filename.endswith(".pptx"):
            ppt_file = os.path.join(directory, filename)
            txt_file = os.path.splitext(filename)[0] + '.txt'  
      
            text = ppt_to_text(ppt_file)
       
            with open(os.path.join(text_folder, txt_file), 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Converted {filename} to {txt_file} and saved in text_files folder")

if __name__ == "__main__":
    directory = parent_directory + '/Datasets/Lecture Content/COMP 6461/Lectures/'
    main(directory)