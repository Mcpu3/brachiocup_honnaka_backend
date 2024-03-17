import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1.dependencies import get_database
from api.v1 import cruds, schemas


api_router = APIRouter(prefix="/groups", tags=["Groups"])

@api_router.get("/{group_uuid}", response_model=schemas.groups.Group)
def get_group(group_uuid: str, database: Session=Depends(get_database)) -> schemas.groups.Group:
    group = cruds.groups.read_group(database, group_uuid)
    if not group:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return group

@api_router.post("/new")
def post_group(request: schemas.groups.NewGroup, _request: Request, database: Session=Depends(get_database)):
    group = cruds.groups.create_group(database, request)
    if not group:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    response = {
        "Location": urllib.parse.urljoin(_request.url._url, f"./group/{group.group_uuid}")
    }

    return JSONResponse(response, status.HTTP_201_CREATED)