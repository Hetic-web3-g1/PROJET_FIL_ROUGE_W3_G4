from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader

from src.database.db_engine import engine

from ..roles import service as role_service
from ..roles.schemas import Right, ServicesRights
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

        if not self._has_right(user.role_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have the right to access this service",
            )

        return user

    def _has_right(self, role_id: int) -> bool:
        if not self.service_rights:
            return True
        with engine.begin() as conn:
            user_role = role_service.get_role_by_id(conn, role_id)

        for service, right in self.service_rights.items():
            if service not in user_role.service_rights:
                return False
            elif (
                user_role.service_rights[service] == Right.VIEWER
                and right == Right.EDITOR
            ):
                return False

        return True
