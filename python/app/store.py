import chromadb
from pathlib import Path

from embeddings import embed_text

CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = 'minecatalog'

_client = None

def get_collection():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

def index(chunks):
    collection = get_collection()
    ##Controlar si es la mejor implementación o es mejor borrar y recrear.
    collection.upsert(
        ids=[c["id"] for c in chunks],
        documents=[c["texto"] for c in chunks],
        embeddings=embed_text([c["texto"] for c in chunks]),
        metadatas=[{"archivo_origen": c["archivo_origen"]} for c in chunks],
    )
    
def search(query, top_k=3):
    collection = get_collection()
    res = collection.query(query_embeddings=embed_text([query]), n_results=top_k)
    salida = []
    
    for doc, meta, dis, cid in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0], res["ids"][0]
    ):
        salida.append({
            "texto": doc,
            "archivo_origen": meta["archivo_origen"],
            "id": cid,
            "score": 1 - dis,  # distancia coseno, necesita convertir a similitud
        })
        
    return salida


if __name__ == "__main__":
    from loader import load_general
    from chunker import chunk_docs
    chunks = chunk_docs(load_general())
    index(chunks)
    print("indexados:", get_collection().count())
    
    for r in search("no puedo entrar a mi cuenta", top_k=3):
        print(round(r["score"], 3), "|", r["archivo_origen"], "|", r["id"])
        print("  ", r["texto"][:80].replace("\n", " "))