from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool

from db.database import Base, engine
from models import model
from services.service import router as service_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await run_in_threadpool(Base.metadata.create_all, bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(service_router)
