from fastapi import FastAPI

app = FastAPI(title= "MineCatalog")

@app.get('/health')
def health():
    return {"status": "ok"}