from fastapi import FastAPI, HTTPException, Request
from rag_system.system import RagManager
from pydantic import BaseModel
from typing import List
from utils.utils import LogsInfo

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
        rag_system = RagManager(Data.model_name, Data.file_paths)
        response = rag_system.generate(Data.query)
        return RequestOutput(answer=response)

    except HTTPException as e:
        LogsInfo(str(e), "API", status_code=e.status_code).save()
        raise

    except Exception as e:
        LogsInfo(str(e), "API", status_code=500).save()
        raise HTTPException(
            status_code=500,
            detail= "Error in server RAG."
        )
