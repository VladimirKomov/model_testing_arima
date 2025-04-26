from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from app.core.logger import logger
from app.routers.routers import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.success("FastAPI is running")
    yield
    logger.success("FastAPI is stopping")

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=False)