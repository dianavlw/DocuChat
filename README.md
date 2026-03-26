# DocuChat

DocuChat is an Ai-Powered document that answers question about uploaded PDFs using Retrieval-Augmented Generation(RAG)

DocuChat allows users to upload PDF documents and ask question about their contents.

The system extracts text from the document, stores embedding in a vector database (ChromaDB), retrieves relevant sections, and uses an LLM to generate grounded in the document.

This application will allow uses to upload PDFs, extract text from the document, and split the document into smaller chunks. Each chuch will be converted into an embedding, the embeddings are store in the ChromaDB. Users will be allowed to ask questions and retrieve the relevant chuncks thats sent to the LLM(Large Language Model), and LLM then generates an answer based on the document.

LLM is a type of AI model that is trained to understand and generate human language. Some popular examples are ChatGBT, and Claude.

This is still being built but if you want to follow along or work on it yourself make a clone

#Run the App
pip install -r requirements.txt
streamlit run app.py

you have to create an env and get a key for the api ai platform: https://platform.openai.com/api-keys

Quick Update:

After testing my application , I made a key decision to use Local Embedding.
Originally this project use openAI, but there were two drawbacks:

1. Api cost for every document uploaded
2. repeated embedding calls due to streamlit reruns

I made an improvement where the sistem was updated to use LOCAL EMBEDDING.

1. sentence-transformers
2. model-all-MiniLM-L6-v2

-This will cost use nothing
-faster processing (runs locally)
-no repeated external calls and better privacy

The tech used for this application:
PYTHON
STREAMlit(UI)
CHROMADB
SENTENCETRANSFORMERS
OPENAI API
PYPDF

How to install:
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
pip install -r requirements.txt

Run the App:
streamlit run app.py

then open: http://localhost:8501
