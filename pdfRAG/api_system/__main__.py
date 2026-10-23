import uvicorn

if __name__ == "__main__":
    uvicorn.run("api_system.rag_api:app", host="127.0.0.1", port=8011, reload=True)