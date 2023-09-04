from src.utils.log.log_manager import logger


class LogErrorMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
