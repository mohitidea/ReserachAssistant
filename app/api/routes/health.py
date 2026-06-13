from fastapi import APIRouter
from app.core.config import settings

router= APIRouter(tags= ['helath'])

@router.get('/health')
def health_check():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "model": settings.llm_model
    }
