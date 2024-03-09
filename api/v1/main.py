from fastapi import APIRouter, Depends, HTTPException, status
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


@api_router.get("/hello_world")
def get_hello_world() -> str:
    return "hello world"

@api_router.post("/hello_world")
def post_hello_world(request: schemas.Helloworld, database: Session=Depends(_get_database)):
    hello_world = crud.create_hello_world(database, request)
    if not hello_world:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    
    return status.HTTP_201_CREATED