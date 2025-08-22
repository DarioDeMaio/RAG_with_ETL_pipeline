from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
from ingest.utils import read_documents

load_dotenv()

PERSISTENT_DIRECTORY = "chroma_db"

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)

def ingest_documents_on_startup(paths):
    if not paths:
        raise ValueError("No PDF files found in the data directory")

    if not os.path.exists(PERSISTENT_DIRECTORY):
        os.makedirs(PERSISTENT_DIRECTORY, exist_ok=True)
        texts = read_documents(paths)
        if not texts:
            raise ValueError("No text chunks were created after splitting documents")

        print(f"Created {len(texts)} text chunks for embedding")
        try:
            vector_db = Chroma.from_documents(
                documents=texts,
                persist_directory=PERSISTENT_DIRECTORY,
                embedding=embeddings,
                collection_name="my_collection"
            )
        except Exception as e:
            print(f"Error creating Chroma database: {e}")
    else:
        print(f"Database already exists at {PERSISTENT_DIRECTORY}, skipping ingestion", flush=True)
        vector_db = Chroma(
            persist_directory=PERSISTENT_DIRECTORY,
            embedding_function=embeddings,
            collection_name="my_collection"
        )
        return vector_db

    print(f"Ingest completed. Data persisted in {PERSISTENT_DIRECTORY}", flush=True)
    return vector_db
