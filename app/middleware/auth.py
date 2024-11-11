from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from session import get_session  # 确保导入路径正确

class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        key = "admin_login"
        data = get_session(request, key)
        print(f"Session data: {data}")
        if data:
            request.state.isLogin = True
        else:
            request.state.isLogin = False
        response = await call_next(request)
        return response