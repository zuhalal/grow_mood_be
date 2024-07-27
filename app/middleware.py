from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException

import firebase_admin
from firebase_admin import auth
from typing import Optional

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path == '/':
            response = await call_next(request)
            return response
        
        authorization: Optional[str] = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

        token = authorization.split(" ")[1] if len(authorization.split(" ")) == 2 else None
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization format")

        try:
            decoded_token = auth.verify_id_token(token)
            request.state.user = decoded_token
        except firebase_admin.auth.InvalidIdTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid ID token")
        except firebase_admin.auth.ExpiredIdTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired ID token")
        except firebase_admin.auth.RevokedIdTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Revoked ID token")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        response = await call_next(request)
        return response

