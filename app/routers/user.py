from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.models.UserModel import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users(session: Session = Depends(get_session)):
    users = session.query(User).all()
    return users
