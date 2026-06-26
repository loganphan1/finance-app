from fastapi import FastAPI
from backend.routes import transaction, health, auth

app = FastAPI()

app.include_router(transaction.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")