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
