from fastapi import FastAPI, HTTPException, Request
from rag_system.system import RagManager
from pydantic import BaseModel
from typing import List
from utils.utils import LogsInfo
import requests

class RequestInput(BaseModel):
    query: str
    file_paths: List[str]
    model_name: str

class RequestOutput(BaseModel):
    answer: str

app = FastAPI(title="RAG System API")

@app.post("/api/query", response_model=RequestOutput)
async def rag_system_api(request: Request, Data: RequestInput):
    try:
        response = requests.get("http://127.0.0.1:8000/chatbot/fetch-parameters")
        data = response.json()
        rag_system = RagManager(Data.model_name, Data.file_paths, data=data)
        response = rag_system.generate(Data.query)
        return RequestOutput(answer=response)

    except HTTPException as e:
        LogsInfo(str(e), "ERROR", status_code=e.status_code).save()
        raise

    except Exception as e:
        LogsInfo(str(e), "ERROR", status_code=500).save()
        raise HTTPException(
            status_code=500,
            detail= "Error in server RAG."
        )