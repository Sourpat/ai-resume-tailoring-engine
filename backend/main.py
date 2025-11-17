from fastapi import FastAPI

from routers import export, tailor, upload

app = FastAPI(title="AI Resume Tailoring Engine")

app.include_router(upload.router)
app.include_router(tailor.router)
app.include_router(export.router)


@app.get("/")
async def read_root():
    return {"message": "AI Resume Tailoring Engine API"}
