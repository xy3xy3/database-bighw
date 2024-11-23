from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.KnowledgeContentModel import KnowledgeContentModel

import random

test_router = APIRouter()

@test_router.get("/")
async def test_root():
    return {"message": "This is a test endpoint"}

@test_router.get("/insert_random_vectors")
async def insert_random_vectors():
    model = KnowledgeContentModel()
    for i in range(5):
        base_id = 1  # 将 base_id 设置为 1
        content = f"Random content {i}"
        embedding = [random.random() for _ in range(2048)]  # 生成一个长度为 2048 的随机向量
        model.save_with_embedding(base_id=base_id, content=content, embedding=embedding)
    return JSONResponse(content={"message": "5 random vectors inserted successfully"})

@test_router.get("/find_similar_vector")
async def find_similar_vector():
    model = KnowledgeContentModel()
    random_embedding = [random.random() for _ in range(2048)]  # 生成一个长度为 2048 的随机向量
    neighbors = model.get_nearest_neighbors(embedding=random_embedding, top_n=3)
    return {"random_embedding": random_embedding, "neighbors": neighbors}