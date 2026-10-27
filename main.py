
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import router
from app.loaders.database_loader import load_database
from app.config import DB_PATH
from app.services.meeting_service import load_meetings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.database = load_database(DB_PATH)
    app.state.meetings = load_meetings()
    yield


app = FastAPI(
    title="MeetingMind API",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid request. Please check the request body."
        },
    )


app.include_router(router)
