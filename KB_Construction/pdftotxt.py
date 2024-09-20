import os
import PyPDF2
parent_directory = os.path.dirname(os.getcwd())

def pdf_to_text(pdf_file):
    text = ''
    with open(pdf_file, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + '\n'
    return text.strip()

def main(directory):

    # directory = parent_directory + '/Datasets/Lecture Content/COMP 6741/Lectures/'

    text_folder = directory + 'text_files/'
    
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)
    
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_file = os.path.join(directory, filename)
            txt_file = os.path.splitext(filename)[0] + '.txt'
            
            text = pdf_to_text(pdf_file)
            
            with open(os.path.join(text_folder, txt_file), 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Converted {filename} to {txt_file} and saved in text_files folder")

if __name__ == "__main__":
    directory = parent_directory + '/Datasets/Lecture Content/COMP 6461/Readings/'
    main(directory)
