from fastapi import FastAPI
from app.api import profiles, settings

app = FastAPI()

app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["profiles"])
app.include_router(settings.router, prefix="/api/v1/settings", tags=["settings"])

@app.get("/")
async def root():
    return {"message": "Welcome to the laundr.me API"}
