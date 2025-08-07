import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.init_db import ingest_documents, PERSISTENT_DIRECTORY

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is required")

app = FastAPI()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)

qa = None


class Query(BaseModel):
    question: str


@app.on_event("startup")
async def startup_event():
    global qa

    try:
        if not os.path.exists(PERSISTENT_DIRECTORY) or not os.listdir(PERSISTENT_DIRECTORY):
            vector_db = ingest_documents([os.path.join("data", f) for f in os.listdir("data") if f.endswith(".pdf")])
        else:
            vector_db = Chroma(
                persist_directory=PERSISTENT_DIRECTORY,
                embedding_function=embeddings,
                collection_name="my_collection"
            )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_db.as_retriever(search_kwargs={"k": 3})
        )
    except Exception as e:
        print(f"Error during startup: {e}")
        raise


@app.post("/query")
async def query_qa(q: Query):
    global qa
    if qa is None:
        raise HTTPException(status_code=500, detail="QA system not initialized")

    try:
        docs = qa.retriever.get_relevant_documents(q.question)
        result = qa.invoke({"query": q.question})
        answer = result.get("result", "No answer generated")

        retrieved_texts = [doc.page_content for doc in docs]

        return {
            "answer": answer,
            "retrieved_documents": retrieved_texts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "qa_initialized": qa is not None}
