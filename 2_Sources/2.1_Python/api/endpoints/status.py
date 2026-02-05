from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_status():
    status = {"api":"online","llm":"running","chroma":"available"}
    return status
