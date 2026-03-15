import os
import tempfile

import streamlit as st
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import RdfReader

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