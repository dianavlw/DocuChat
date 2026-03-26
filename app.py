import os
import tempfile

import streamlit as st
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from docuchat_utils import extract_text_from_reader, clean_text, chunk_text 

load_dotenv()
#load your variables into the program

api_key = os.getenv("OPENAI_API_KEY")
#reading the environment variable
if not api_key:
    raise ValueError("missing OPENAI_API_KEY in .env file")
#we run test to make sure the program runs, this raises an error letting us know if the key exists.
client = OpenAI(api_key=api_key)
#creating a connection object that will talk to the openAI servers.

#runs machine and is free of charge
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
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
            cleaned = " ".join(page_text.split())
            full_text.append(cleaned)
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


#uses your laptop not the open ai api
def get_embedding(text: str) -> list[float]:
    return embedding_model.encode(text).tolist()

#we check the data in the database, if the count returns more than 0 delete it
#.get() this gets all items

def store_chunks(chunks:list[str], source_name:str)->None:
    #the number of items sotred in the collection 
    existing = collection.count()
    if existing > 0:
        try:
            all_items =collection.get()
          # check if id exist delete previous chunks this will clear the database
            #this must be done so the script doesnt run everything, streamlit tends to do that creating duplicates
            if all_items and all_items.get("ids"):
                collection.delete(ids=all_items["ids"])
                #we must do error handling incase something does go wrong, for now we can ignore
        except Exception:
            pass
        # we must loop trhough the chunks 
        # #ex. i=0, chunk="A", i=1, chunk="B", i=2, chunk="C"
    for i, chunk in enumerate(chunks):
        #converst the chunks into a vector
        embedding = get_embedding(chunk)
        #store in chromadb
        collection.add(
            ids=[f"{source_name}_{i}"],
            documents=[chunk],
            embeddings=[embedding], 
            #stores extra details, information
            metadatas=[{"source": source_name, "chunk_index": i}]
        )

#the question will be converted to embedding, searchde trough Chromadb, and return relevant chunks
def retrieve_chunks(question:str, top_k: int=3):
    query_embedding = get_embedding(question)
    results = collection.query(
        query_embeddings = [query_embedding], 
        #return top 3
        n_results=top_k
    )
    return results 

#user as a string


def answer_question(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
#a list of text is retrieve, combied into one context block
#\n\n adds blank lines between the chunks, we need a block of text not a python list, very important

    #we send a request to the chat model 
        #we want teh response model gpt-4.1-mini
    try:
        #this is the converation, two roles: system and user
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful document assistant. "
                        "Answer only using the provided context. "
                        "If the answer is not in the context, say: "
                        "'I could not find that in the uploaded PDF.'"
                    )
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {e}"

#this creates an upload file botton in the UI
#the user selects pdf file
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
#if the file is not the it will be a file like object
#if we dont do this the app will process the file that does not exist
if uploaded_file is not None:
    #this will create a temporary file on your computer, pdfreader works good with a file type
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        #keep the file around after the block ends so one can still read it
        #the end must be .pdf (the suffix)
        tmp_file.write(uploaded_file.read())
        #copies the uploaded pdf contents into a temp file, and store it
        temp_pdf_path= tmp_file.name
        #the spinner will show while reading the pdf
    with st.spinner("reading pdf..."):
        text = extract_text_from_pdf(temp_pdf_path)
    
    #checking whether the pdf actually had readable text
    #.strip removes whitespaces
    if not text.strip():
        st.error("no readable text found in this pdf.")
    else: 
        #splits the chunks into smaller pieces
        with st.spinner("chunking and indexing document ..."):
            chunks = chunk_text(text)
            #creates embedding, stores in chromadb, adds metadata source file and chunk index
            store_chunks(chunks, uploaded_file.name)
      #show sucess message
        st.success("pdf processed successfully.")

        #the user ask a question
        question = st.text_input("ask a question about the pdf")
        
        #embedd the question, search chromadb, find the most relevant chunks
        if question:
            with st.spinner("searching document and generating answer..."):
                results = retrieve_chunks(question)
                #extract the chunk text
                documents = results["documents"][0]
                metadatas =results["metadatas"][0]
                try:
                  answer = "Top matching chunks shown below (OpenAI disabled)."
                except Exception as e:
                  answer = f"Answer generation failed: {e}"
            
            st.subheader("answer")
            st.write(answer) 

            st.subheader("sources")
            #source:name.pdf, chunk:2 ect.
            #pairs each chunk with its metadata
            for doc, meta in zip(documents, metadatas):
                st.markdown(
            #source filename, chunk number, and a preview of the chunk text
                    f"**Source:** {meta['source']} | **Chunk:** {meta['chunk_index']}"
                ) 
                #show only the first 500 characters so its not too long
                st.write(doc[:500] + ("..." if len(doc) > 500 else ""))
                #adds a divider between the source and chunks
                st.divider()

