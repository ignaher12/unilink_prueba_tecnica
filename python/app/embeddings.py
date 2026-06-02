from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-base"
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def embed_text(textos):
    model = get_model()
    i_textos = [f"passage: {texto}" for texto in textos]
    return model.encode(i_textos, normalize_embeddings=True).tolist()

def embed_query(query):
    model = get_model()
    i_query = f"query: {query}"
    return model.encode([i_query], normalize_embeddings=True)[0].tolist()

if __name__ == "__main__":
    vecs = embed_text(["hola mundo", "error de base de datos"])
    print(len(vecs), "vectores")
    print("dimensión:", len(vecs[0]))   # debería dar 384 con este modelo