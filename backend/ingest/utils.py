from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def read_pdf(path: str, docs: list) -> list:
    if not os.path.exists(path):
            print(f"Warning: File {path} not found, skipping...")
    try:
        loader = PyPDFLoader(path)
        loaded_docs = loader.load()
        docs.extend(loaded_docs)
        print(f"Loaded {len(loaded_docs)} pages from {path}")
    except Exception as e:
        print(f"Error loading {path}: {e}")

def read_csv(path: str, docs: list) -> list:
    if not os.path.exists(path):
            print(f"Warning: File {path} not found, skipping...")
    try:
         loader = CSVLoader(path)
         loaded_docs = loader.load()
         docs.extend(loaded_docs)
         print(f"Loaded {len(loaded_docs)} pages from {path}")
    except Exception as e:
        print(f"Error loading {path}: {e}")
    
def split_documents(docs: list) -> list:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(docs)
    return texts

def read_documents(paths: str) -> list:
    docs = []
    for path in paths:
        if path.endswith(".pdf"):
            read_pdf(path, docs)

    if not docs:
        raise ValueError("No documents were successfully loaded from the PDF files")
    
    docs = split_documents(docs)
    return docs
