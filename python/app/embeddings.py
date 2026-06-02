from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def embed_text(textos):
    model = get_model()
    return model.encode(textos, normalize_embeddings=True, show_progress_bar=True).tolist()

if __name__ == "__main__":
    vecs = embed_text(["hola mundo", "error de base de datos"])
    print(len(vecs), "vectores")
    print("dimensión:", len(vecs[0]))   # debería dar 384 con este modelo