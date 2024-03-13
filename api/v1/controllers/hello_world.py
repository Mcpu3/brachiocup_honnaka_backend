import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1.dependencies import get_database
from api.v1 import cruds, schemas


api_router = APIRouter(prefix="/hello_world", tags=["Hello World"])

@api_router.get("/{hello_world_uuid}", response_model=schemas.hello_world.HelloWorld)
def get_hello_world(hello_world_uuid: str, database: Session=Depends(get_database)) -> schemas.hello_world.HelloWorld:
    hello_world = cruds.hello_world.read_hello_world(database, hello_world_uuid)
    if not hello_world:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return hello_world

@api_router.post("/")
def post_hello_world(request: schemas.hello_world.HelloWorld, _request: Request, database: Session=Depends(get_database)):
    hello_world = cruds.hello_world.create_hello_world(database, request)
    if not hello_world:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    response = {
        "Location": urllib.parse.urljoin(_request.url._url, f"./hello_world/{hello_world.uuid}")
    }

    return JSONResponse(response, status.HTTP_201_CREATED)
