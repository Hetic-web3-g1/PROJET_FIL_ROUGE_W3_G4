from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader

from ..roles.schemas import ServicesRights
from . import service as auth_service


class CustomSecurity:
    def __init__(self, service_rights: ServicesRights = {}):
        self.service_rights = service_rights

    def __call__(
        self,
        request: Request,
        authorization: str = Depends(APIKeyHeader(name="Authorization")),
    ):
        token = authorization.split(" ").pop()
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            user = auth_service.verify_jwt_token(token)
        except auth_service.InvalidToken:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

