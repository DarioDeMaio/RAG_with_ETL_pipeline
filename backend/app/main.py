import os
import asyncio
from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from ingest.add_to_db import ingest_documents_on_startup, PERSISTENT_DIRECTORY, embeddings, llm, update_croma_db
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:4200"]

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is required")

qa = None

class QueryRequest(BaseModel):
    question: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    global qa
    try:
        if not os.path.exists(PERSISTENT_DIRECTORY) or not os.listdir(PERSISTENT_DIRECTORY):
            vector_db = ingest_documents_on_startup([os.path.join("data", f) for f in os.listdir("data") if f.endswith(".pdf")])
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
        yield
    except Exception as e:
        print(f"Error during startup: {e}")
        raise
    finally:
        print("Shutting down startup event...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query_qa(request: QueryRequest):
    global qa
    if qa is None:
        raise HTTPException(status_code=500, detail="QA system not initialized")

    try:
        docs = qa.retriever.get_relevant_documents(request.question)
        result = qa.invoke({"query": request.question})
        answer = result.get("result", "No answer generated")

        retrieved_texts = [doc.page_content for doc in docs]

        return {"answer": answer, "retrieved_documents": retrieved_texts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "qa_initialized": qa is not None}

async def trigger_ingest_flow(bucket: str, key: str, dest: str="tmp"):
    update_croma_db(bucket, key, dest)

@app.post("/minio/webhook")
async def minio_webhook(request: Request, authorization: str = Header(None)):
    event = await request.json()
    print("Evento MinIO:", event)

    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    asyncio.create_task(trigger_ingest_flow(bucket, key))
    return {"status": "ok"}
