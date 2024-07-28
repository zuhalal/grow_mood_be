from app.utils.response_generator import ResponseGenerator
from fastapi import APIRouter
from app.model.recommendation import RecommendationRequest
from app.utils.db import db
from fastapi.responses import JSONResponse

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
    try:
        output = agent.generate_answer(db=db, question=f"Please provide the top food recommendations for people that feel {req.mood} and {req.description}")
        return {"recommendation": output, "total": len(output)}
    except Exception as e:
        print(e)

@router.post("/recommendation2")
async def create_item2(req: RecommendationRequest):
    agent = ResponseGenerator()
    try:
        output = await agent.get_foods(questions=f"Please provide the top food recommendations for people that feel {req.mood} and {req.description}")
        return JSONResponse(content={"recommendation": output})
    except Exception as e:
        print(e)