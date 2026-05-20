from fastapi import FastAPI

from app.routes import items

app = FastAPI()
app.include_router(items.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok update vs2"}
