import os
import tempfile

import streamlit as st
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv()
#load your variables into the program

api_key = os.getenv("OPENAI_API_KEY")
#reading the environment variable
if not api_key:
    raise ValueError("missing OPENAI_API_KEY in .env file")
#we run test to make sure the program runs, this raises an error letting us know if the key exists.
client = OpenAI(api_key=api_key)
#creating a connection object that will talk to the openAI servers.

#streamlit 
#create a browser tab title
st.set_page_config(page_title="DocuChat", page_icon="📄")
#make a icon 
st.title("📄 DocuChat")
#display text
st.write("Upload a pdf and ask question about it.")

#create a chrome cliet
chroma_client=chromadb.Client()
collection = chroma_client.get_or_create_collection(name="docuchat_chunks")

#Chroma database is where my chatbot will store data, ex. chunks from the PDF

def extract_text_from_pdf(file_path:str) -> str:
    reader = PdfReader(file_path)
    full_text = []
#from pypdf import PdfReader - what this does is loads a tool from the library so we can use it in our code
#pypdf lets u work with pdf files, it can read, extract text, split, merge pdf and inspect pages
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text.append(page_text)
    return "\n".join(full_text)
    
#funtion takes in three inputs, 800 charactes each chunk, it overlaps to prevent losing context
#returns an array of chunks, starting at 0 up to 800
#it ends once it has reached chunk_size
#with the overlap it prevents from spilling 
#with overlapping chunks share text that may contain important text retrieval becomes more reliable
def chunk_text(text:str, chunk_size: int= 800, overlap:int= 150)->list[str]:
    chunks = []
    start = 0

    while start <len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
