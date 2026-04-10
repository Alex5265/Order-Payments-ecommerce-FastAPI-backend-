from fastapi import FastAPI, Depends

from app.api.routers import categories
from app.core.config import Settings, get_settings

app = FastAPI(
    title='FastAPI Order/Payments API',
    version='0.1.0',
)

app.include_router(categories.router)


@app.get("/")
async def root():
    """
    Basic route showing that the API is working
    """
    return {"message": "Welcome to the Order/Payments ecommerce API"}

@app.get("/settings")
async def get_app_settings(settings: Settings = Depends(get_settings)):
    return {
        "app_name":settings.app_name,
        "envierment":settings.environment,
        "postgress_db":settings.postgres_db
    }