from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import chat, health, query, document
app= FastAPI(title= settings.app_name)
app.include_router(health.router)
app.include_router(query.router)
app.include_router(document.router)
app.include_router(chat.router)

@app.get('/')
async def root():
    return {"message": f"{settings.app_name} is running"}
