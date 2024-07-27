import firebase_admin

from app.router import router
from app.middleware import FirebaseAuthMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, firestore
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from app.config import get_settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

app.add_middleware(FirebaseAuthMiddleware)
app.include_router(router)

settings = get_settings()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(settings.firebase_config_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
