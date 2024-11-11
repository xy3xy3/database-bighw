from fastapi import Request, HTTPException
from functools import wraps

from fastapi.responses import RedirectResponse

def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        print(f"Decorator accessed request: {request}")

        if not request or not hasattr(request.state, "isLogin") or not request.state.isLogin:
            if request.method == "GET":
                # 如果是GET请求，重定向到登录页面
                return RedirectResponse(url="/admin/login", status_code=302)
            else:
                # 如果是POST请求，返回401 Unauthorized
                raise HTTPException(status_code=401, detail="未授权")

        return await func(*args, **kwargs)
    return wrapper