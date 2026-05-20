from fastapi import FastAPI

from app.routes import items

app = FastAPI()
app.include_router(items.router)



@app.get("/health")
def health():
    return {"status": "ok", "version": "v2-gitops-test"}
