from fastapi import FastAPI
from app.endpoints.api.v1.ticker_routers import router as ticker_router

app = FastAPI(title="TestWork FastAPI application", description="TestWork FastAPI application")


app.include_router(ticker_router)