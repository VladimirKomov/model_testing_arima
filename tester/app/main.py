import uvicorn
from fastapi import FastAPI
from app.core.logger import logger
from app.routers.routers import router

app = FastAPI()
app.include_router(router)

logger.success("FastAPI is running")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)