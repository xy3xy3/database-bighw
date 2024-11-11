from passlib.context import CryptContext
from fastapi.responses import JSONResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, pwd: str) -> bool:
    return pwd_context.verify(plain_password, pwd)
# ajax返回封装
def response(code: int, message: str, data: dict = None):
    return JSONResponse(content={"code": code, "msg": message, "data": data}, status_code=200)

def res_suc(message: str, data: dict = None):
    return response(0, message, data)

def res_err(message: str, data: dict = None):
    return response(1, message, data)