import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1 import crud, models, schemas
from api.v1.database import LocalSession, engine


models.Base.metadata.create_all(engine)

api_router = APIRouter()

def _get_database():
    database = LocalSession()
    try:
        yield database
    finally:
        database.close()


@api_router.get("/hello_world/{hello_world_uuid}", response_model=schemas.HelloWorld, tags=["hello_world"])
def get_hello_world(hello_world_uuid: str, database: Session=Depends(_get_database)) -> schemas.HelloWorld:
    hello_world = crud.read_hello_world(database, hello_world_uuid)
    if not hello_world:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return hello_world

@api_router.post("/hello_world", tags=["hello_world"])
def post_hello_world(request: schemas.HelloWorld, _request: Request, database: Session=Depends(_get_database)):
    hello_world = crud.create_hello_world(database, request)
    if not hello_world:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    response = {
        "Location": urllib.parse.urljoin(_request.url._url, f"./hello_world/{hello_world.uuid}")
    }

    return JSONResponse(response, status.HTTP_201_CREATED)
