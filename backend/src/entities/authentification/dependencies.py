from fastapi import Request, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from .schemas import ServicesRights
from . import service as auth_service
from ..users.schemas import User
from ..masterclasses.models import masterclass_user_table


class CustomSecurity:
    def __init__(self, service_rights: ServicesRights = {}, is_admin: bool = False):
        self.service_rights = service_rights
        self.use_is_admin = is_admin

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
        
        if self.use_is_admin and not self.is_admin(user):  # Check if user is admin when is_admin is True
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges",
            )

        return user


    @staticmethod
    def is_admin(user: User):
        """
        Check if the user is an admin.

        Args:
            user (User, optional): The user to check.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        if user.role != 'admin':
            return False
        return True