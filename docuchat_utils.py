from typing import List

def extract_text_from_reader(reader)-> str:
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)
    return "\n".join(pages_text).strip()
def clean_text(text:str) -> str:
    return " ".join(text.split()).strip()

def chunk_text(text:str, chunk_size: int = 500, overlap: int = 100) ->List[str]:
    if not text.strip():
        return []
    
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    
    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

