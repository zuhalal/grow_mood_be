from fastapi import APIRouter

router =  APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/protected")
async def protected_route():
    return {"message": "This is a protected route"}
