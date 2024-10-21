from sqlmodel import SQLModel, create_engine, Session
from config import settings
from models.CategoryModel import CategoryModel
from models.ConfigModel import ConfigModel
from models.OrderModel import OrderModel
from models.PaymentModel import PaymentModel
from models.ProductModel import ProductModel
from models.UserModel import UserModel
from utils import hash_password

engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db():
    # 创建表结构
    SQLModel.metadata.create_all(engine)

    # 在ConfigModel创建k,v管理员
    with Session(engine) as session:
        admin_config = ConfigModel(k="admin", v="admin")
        session.add(admin_config)
        session.commit()
def get_session():
    with Session(engine) as session:
        yield session
