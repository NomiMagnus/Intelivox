from fastapi import FastAPI
from app.api.endpoints import router
from app.config import settings

app = FastAPI(
    title="Intelivox Resident Management API",
    version="0.1.0",
    description="REST API for receiving telephony webhook events and managing interaction updates."
)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    settings.ensure_data_paths()
