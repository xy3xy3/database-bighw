from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models.UserModel import UserModel

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users(session: Session = Depends(get_session)):
    users = session.exec(UserModel).all()
    return users
