from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from app import schemas
from app.db.session import get_db_session
from app.service import (
    fetch_car_makes,
    fetch_car_make,
    fetch_make_models,
    InvalidMakeException,
)

description = """
A REST API that provides an extensive catalog of car makes and models.
In case you happen to find a make or model not available in the API, please let me know from 
the contact link below and I'll add it ASAP.
"""

app = FastAPI(
    title="Car makes and models API",
    description=description,
    version="0.0.1",
    contact={"name": "Dennis Wainaina", "email": "dennis@byteslab.io"},
    redoc_url=None,
)


@app.exception_handler(InvalidMakeException)
def invalid_car_make_exception(request: Request, exc: InvalidMakeException):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.get("/", include_in_schema=False)
async def root():
    return "Cars API"


@app.get("/makes", response_model=list[schemas.CarMake])
def get_car_makes(search: str = None, session: Session = Depends(get_db_session)):
    """
    Lists all car makes. If `search` is present, makes containing that term will be filtered.
    """
    return fetch_car_makes(session, search)


@app.get("/makes/{make_id}", response_model=schemas.CarMake)
def get_car_make(make_id: str, session: Session = Depends(get_db_session)):
    """
    Returns a single car make.
    """
    return fetch_car_make(session, make_id)


@app.get("/makes/{make_id}/models", response_model=list[schemas.CarModel])
def get_make_models(make_id: str, session: Session = Depends(get_db_session)):
    """
    Returns a list of models for a given car make.
    """
    return fetch_make_models(session, make_id)
