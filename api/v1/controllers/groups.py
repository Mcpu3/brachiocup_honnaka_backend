import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1 import cruds, models, schemas
from api.v1.dependencies import get_database, get_current_user


api_router = APIRouter(prefix="/me/groups", tags=["Groups"])

@api_router.get("/{group_uuid}", response_model=schemas.groups.Group)
def get_group(group_uuid: str, database: Session=Depends(get_database)) -> schemas.groups.Group:
    group = cruds.groups.read_group(database, group_uuid)
    if not group:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return group

@api_router.post("/signup")
def post_group(request: schemas.groups.NewGroup, _request: Request, current_user: models.User=Depends(get_current_user), database: Session=Depends(get_database)):
    group = cruds.groups.create_group(database, current_user, request)
    if not group:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    response = {
        "Location": urllib.parse.urljoin(_request.url._url, f"./group/{group.group_uuid}")
    }

    return JSONResponse(response, status.HTTP_201_CREATED)
