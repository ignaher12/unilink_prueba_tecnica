from fastapi import FastAPI
from pydantic import BaseModel

from app.loader import load_general
from app.chunker import chunk_docs
from app.store import index, search

app = FastAPI(title= "MineCatalog")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3
    
@app.get('/health')
def health():
    return {"status": "ok"}

@app.post('/ingest')
def ingest():
    docs = load_general()
    chunks = chunk_docs(docs)
    index(chunks)
    return {"indexed": len(chunks)}

@app.post('/search')
def search_endp(req: SearchRequest):
    results = search(req.query, req.top_k)
    return {"query": req.query, "resultados": results}