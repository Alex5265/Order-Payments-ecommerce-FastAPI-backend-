from fastapi import FastAPI

from app.api.routers import categories

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
