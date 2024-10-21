from fastapi import APIRouter, Depends
from models.UserModel import UserModel

router = APIRouter(prefix="/users", tags=["users"])