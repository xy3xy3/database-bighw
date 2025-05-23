import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from session import get_session  # 确保导入路径正确

class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        key = "admin_login"
        try:
            data = get_session(request, key)
            print(f"Session data: {data}")
            request.state.isAdminLogin = bool(data)
        except Exception as e:
            logging.error(f"Middleware error: {e}", exc_info=True)
            request.state.isAdminLogin = False
        response = await call_next(request)
        return response