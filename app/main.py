from fastapi import FastAPI

app = FastAPI(
    title='FastAPI Order/Payments API',
    version='0.1.0',
)


@app.get("/")
async def root():
    """
    Basic route showing that the API is working
    """
    return {"message": "Welcome to the Order/Payments ecommerce API"}
