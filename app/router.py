from app.utils.response_generator import ResponseGenerator
from fastapi import APIRouter
from app.model.recommendation import RecommendationRequest
from app.utils.db import db

router =  APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/protected")
async def protected_route():
    return {"message": "This is a protected route"}

@router.post("/recommendation")
async def create_item(req: RecommendationRequest):
    agent = ResponseGenerator()
    print("masook")
    try:
        output = agent.generate_answer(db=db, question=f"Please provide the top food recommendations for people that feel {req.mood} and {req.description}")
        return {"recommendation": output, "total": len(output)}
    except Exception as e:
        print(e)