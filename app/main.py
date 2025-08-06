import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from chromadb.config import Settings


load_dotenv()
persist_directory = "chroma_db"
settings = Settings(
    persist_directory=persist_directory
)
app = FastAPI()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

llm = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18",
    temperature=0
)

vector_db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings,
    client_settings=settings
)

retriever = vector_db.as_retriever()

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="map_reduce", retriever=vector_db.as_retriever())

class Query(BaseModel):
    question: str

@app.post("/query")
async def query_qa(q: Query):
    res = qa.invoke(q.question)
    return {"answer": res}

def ingest_documents(pdf_paths):
    docs = []

    for path in pdf_paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(docs)

    vector_db.add_documents(texts)
    vector_db.persist()

if __name__ == "__main__":
    if not os.path.exists(persist_directory) or not os.listdir(persist_directory):
        pdf_files = [os.path.join("data", f) for f in os.listdir("data") if f.endswith(".pdf")]
        ingest_documents(pdf_files)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
