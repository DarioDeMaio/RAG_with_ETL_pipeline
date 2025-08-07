from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
import os

PERSISTENT_DIRECTORY = "chroma_db"

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)


def ingest_documents(paths):
    if not paths:
        raise ValueError("No PDF files found in the data directory")

    docs = []
    for path in paths:
        if path.endswith(".pdf"):
            if not os.path.exists(path):
                print(f"Warning: File {path} not found, skipping...")
                continue
            try:
                loader = PyPDFLoader(path)
                loaded_docs = loader.load()
                docs.extend(loaded_docs)
                print(f"Loaded {len(loaded_docs)} pages from {path}")
            except Exception as e:
                print(f"Error loading {path}: {e}")
                continue

    if not docs:
        raise ValueError("No documents were successfully loaded from the PDF files")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(docs)

    if not texts:
        raise ValueError("No text chunks were created after splitting documents")

    print(f"Created {len(texts)} text chunks for embedding")

    os.makedirs(PERSISTENT_DIRECTORY, exist_ok=True)

    try:
        vector_db = Chroma.from_documents(
            documents=texts,
            persist_directory=PERSISTENT_DIRECTORY,
            embedding=embeddings,
            collection_name="my_collection"
        )
    except Exception as e:
        print(f"Error creating Chroma database: {e}")
        vector_db = Chroma(
            persist_directory=PERSISTENT_DIRECTORY,
            embedding_function=embeddings,
            collection_name="my_collection"
        )
        vector_db.add_documents(texts)

    print(f"Ingest completed. Data persisted in {PERSISTENT_DIRECTORY}", flush=True)
    return vector_db
