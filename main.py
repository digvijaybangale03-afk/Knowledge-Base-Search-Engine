from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from backend.ingest_file import ingest_file
import uvicorn
import os, uuid, io, json
from backend.ingest_file import ingest_file
from backend.utils import chunk_text, ensure_dirs
from backend.query import answer_query

app = FastAPI(title="Knowledge-base RAG API")

@app.post("/ingest")
async def ingest(file: UploadFile = File(...), source: str = Form(None)):
    contents = await file.read()
    name = file.filename or f"file-{uuid.uuid4().hex}.bin"
    saved_path = os.path.join(os.getcwd(), "data", name)
    os.makedirs(os.path.dirname(saved_path), exist_ok=True)
    with open(saved_path, "wb") as f:
        f.write(contents)
    n_docs = ingest_file(saved_path, source=source)
    return {"status":"ok","ingested_documents": n_docs, "filename": name}

@app.post("/query")
async def query(q: str = Form(...), top_k: int = Form(5)):
    resp = answer_query(q, top_k=top_k)
    return JSONResponse(content=resp)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
