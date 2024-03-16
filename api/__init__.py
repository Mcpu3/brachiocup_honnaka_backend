import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import models
from api.v1.controllers import hello_world
from api.v1.controllers import groups
from api.v1.database import engine


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(hello_world.api_router, prefix="/api/v1")
app.include_router(groups.api_router, prefix="/api/v1")

models.Base.metadata.create_all(engine)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.AsgiMiddleware(app).handle(req, context)
