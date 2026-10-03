from fastapi import FastAPI

app = FastAPI(title="NoteMind API")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to NoteMind API"}
