from fastapi import FastAPI
from app.routers import user, product, order, admin

app = FastAPI(title="在线购物系统")

app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "欢迎使用在线购物系统"}
