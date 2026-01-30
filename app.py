from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "FrankenAgent beats all"}

@app.get("/health")
def health():
    return {"status": "alive"}
