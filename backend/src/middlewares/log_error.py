import logging
import traceback

from fastapi.responses import JSONResponse
from starlette.middleware import base

from config import settings


class LogErrorMiddleware(base.BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logging.error(e, exc_info=True, stack_info=True)
            if settings.environment == "production":
                response_content = {"detail": "Unexpected error"}
            else:
                response_content = {"detail": traceback.format_exc()}

            return JSONResponse(
                status_code=500,
                content=response_content,
            )
