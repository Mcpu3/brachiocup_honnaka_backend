import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import models
from api.v1.controllers import groups, users, balances, item_groups, item_purchasing, item_purchasing_histories
from api.v1.database import engine


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(users.api_router, prefix="/api/v1")
app.include_router(groups.api_router, prefix="/api/v1")
app.include_router(balances.api_router, prefix="/api/v1")
app.include_router(item_groups.api_router, prefix="/api/v1")
app.include_router(item_purchasing.api_router, prefix="/api/v1")
app.include_router(item_purchasing_histories.api_router, prefix="/api/v1")

models.Base.metadata.create_all(engine)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.AsgiMiddleware(app).handle(req, context)
