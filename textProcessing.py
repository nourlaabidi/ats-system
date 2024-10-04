from nltk.tokenize import word_tokenize
import string
from docx import Document
import fitz
import openai
import re
import nltk
#this function will extract the text from the document with .docx format
def extract_text_from_docx(file_path):
       doc = Document(file_path)
       text = []
       for paragraph in doc.paragraphs:
           text.append(paragraph.text)
       return '\n'.join(text)
#this function will extract the text from the document with .pdf format
def extract_text_from_pdf(file_path):
    pdf_document = fitz.open(file_path)
    text = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text.append(page.get_text())
    return '\n'.join(text)
#this function combines the two previous functions and cleans the text 
def process_file(file_path):
    nltk.download('punkt_tab')
    text = ""
    if file_path.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file type")

    tokens = word_tokenize(text)
    clean_tokens = [token for token in tokens if token not in string.punctuation]
    clean_text = ' '.join(clean_tokens)
    return clean_text
#this function will clean the json response format
def clean_json_response(response_content):
    response_content = re.sub(r'(?<!")(\bName\b|\bSkills\b|\bTechnologies\b|\bSpeaking languages\b|\bWork experience\b)(?!")',r'"\1"',response_content)
 
    response_content = response_content.replace("\\", '')
    response_content = response_content.replace("/", '')
    response_content = response_content.replace('\u00bd', '1/2').replace('\u00b0', '°').replace('\u00a9', '(c)').replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
 
    response_content = re.sub(r'(?<=: )"(.*?)(?<!\\)"', lambda match: '"' + match.group(1).replace('"', '\\"') + '"', response_content)
    if not response_content.strip().endswith('}'):
        response_content += '}]'
    return response_content
def none_if_empty(item):
  if item == '':
    return "null"
  else:
    return item
#this function transform a text to a vector of embedings using the model "text-embedding-ada-00"
def get_embedding(text):
    get_embeddings_response = openai.Embedding.create(
        input=text,
        engine="text-embedding-ada-002"
    )
    return get_embeddings_response.data[0].embedding