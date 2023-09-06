import logging
import traceback

from fastapi.responses import JSONResponse

from config import settings


class LogErrorMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            await self.app(scope, receive, send)
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
