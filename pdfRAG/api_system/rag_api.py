from fastapi import FastAPI, HTTPException
from rag_system.system import RagManager
from pydantic import BaseModel
from typing import List

class RequestInput(BaseModel):
    query: str
    file_paths: List[str]
    # user_id: str
    # conversation_id: str

class RequestOutput(BaseModel):
    answer: str

app = FastAPI(title="RAG System API")

@app.post("/api/query", response_model=RequestOutput)
async def rag_system_api(Data: RequestInput):
    try:
        rag_system = RagManager(Data.file_paths)
        response = rag_system.generate(Data.query)
        return RequestOutput(answer=response)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail= "Error in server RAG."
        )