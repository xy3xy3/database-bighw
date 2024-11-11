from itsdangerous import URLSafeTimedSerializer
from fastapi import Request, Response

SECRET_KEY = "test123"
serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_session(response: Response, key, data):
    value = serializer.dumps(data)
    response.set_cookie(key=key, value=value, httponly=True, max_age=3600)

def get_session(request: Request, key):
    value = request.cookies.get(key)
    if not value:
        return None
    try:
        data = serializer.loads(value, max_age=3600)
        return data
    except:
        return None

def clear_session(response: Response):
    response.delete_cookie("session_token")
