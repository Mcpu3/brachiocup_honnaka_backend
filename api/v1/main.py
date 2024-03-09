from fastapi import APIRouter


api_router = APIRouter()

@api_router.get("/hello_world")
def get_hello_world() -> str:
    return "hello world"