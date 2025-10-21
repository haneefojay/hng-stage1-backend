from fastapi import FastAPI
from app.database import engine, Base
from app import routes
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="HNG Stage 1 Task - String Analyzer Service")

@app.get("/")
def root():
    return {"message": "String Analyzer API is running"}

app.include_router(routes.router)

@app.on_event("startup")
async def on_startup():
    logger.info("Creating database tables (if not exist)...")
    async with engine.begin() as conn:
        # import models module so they are registered on Base.metadata
        from app import models  # noqa
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Startup complete.")