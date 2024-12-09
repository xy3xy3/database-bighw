import asyncio
from datetime import datetime
import json
from fastapi import APIRouter, File, Request, Form, UploadFile
from typing import List, Optional

from fastapi.responses import JSONResponse
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from utils import list_to_vector
from tools.ai import ai
from models.KnowledgeContentModel import KnowledgeContentModel
from models.KnowledgeBaseModel import KnowledgeBaseModel
from fastapi.templating import Jinja2Templates
import os
import shutil
from tools.LoadMd import load_markdown_to_documents, split_documents_by_token

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter()

# 知识库列表页面
@router.get("/knowledgecontent")
@login_required
async def knowledgecontent_list(request: Request):
    model = KnowledgeBaseModel()
    mapping = await model.get_map("id","name")
    knowledgebases = await model.get_options_list("id", "name")  # 获取知识库列表
    return templates.TemplateResponse("knowledgecontent.html", {"request": request,"mapping":mapping, "knowledgebases": knowledgebases})

# 知识库表单页面
@router.get("/knowledgecontent_form")
@login_required
async def knowledgecontent_form(request: Request):
    model = KnowledgeBaseModel()  # 实例化知识库数据访问对象
    knowledgebases = await model.get_options_list("id", "name")  # 获取知识库列表
    return templates.TemplateResponse("knowledgecontent_form.html", {"request": request, "knowledgebases": knowledgebases})

# 知识库导入文件
@router.get("/knowledgecontent_import")
@login_required
async def knowledgecontent_import(request: Request):
    model = KnowledgeBaseModel()  # 实例化知识库数据访问对象
    knowledgebases = await model.get_options_list("id", "name")  # 获取知识库列表
    return templates.TemplateResponse("knowledgecontent_import.html", {"request": request, "knowledgebases": knowledgebases})
@router.post("/knowledgecontent_import")
@login_required
async def knowledgecontent_import_post(
    request: Request,
    base_id: int = Form(...),
    max_len: int = Form(...),
    over_leap: int = Form(...),
    file_path: Optional[str] = Form(None),
):
    # 异步处理导入任务
    asyncio.create_task(process_import_task(base_id, max_len, over_leap, file_path))

    return ResponseModel(code=0, msg="成功")

def split_json(file_path: str, max_len: int, over_leap: int) -> List[str]:
    #   读取列表qa对
    res = []
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    for item in data:
        question = item.get("question", "")
        answer = item.get("answer", "")

        # 合并问题和答案
        merged_text = f"问题：{question}\n答案：{answer}"
        res.append(merged_text)

    return res
def split_md(file_path: str, max_len: int, over_leap: int) -> List[str]:
    """
    根据给定的文件路径、最大长度和重叠量，拆分 Markdown 文件内容。

    参数:
    file_path (str): Markdown 文件的路径。
    max_len (int): 每个块的最大长度（以 token 为单位）。
    over_leap (int): 块之间的重叠长度（以 token 为单位）。

    返回:
    List[str]: 拆分后的文本块列表。
    """
    # 加载 Markdown 文件并转换为 Document 对象
    documents = load_markdown_to_documents(file_path)

    # 基于 token 进行拆分
    split_texts = split_documents_by_token(documents, chunk_size=max_len, chunk_overlap=over_leap)

    return split_texts

async def process_import_task(base_id:int,max_len: int, over_leap: int, file_path: Optional[str]):
    knowledegebase_model = KnowledgeBaseModel()
    content_model = KnowledgeContentModel()
    embedding_model = await knowledegebase_model.get_model_details_by_base_id(base_id)
    # 调用切割函数获取拆分后的文本列表
    # 获取文件后缀
    ext = os.path.splitext(file_path)[1]
    if not file_path:
        res = []
        print("文件路径为空")
        return
    if ext == ".md" or ext == ".txt":
        res = split_md(file_path, max_len, over_leap)
    elif ext == ".json":
        res = split_json(file_path, max_len, over_leap)
    print(res)
    aiApi = ai(embedding_model['api_key'],embedding_model['base_url'])
    model_name = embedding_model['model']
    for context in res:
        print(f"插入{context}")
        embedding = await aiApi.embedding(model_name, context)
        data = {
            "base_id": base_id,
            "content": context,
            "embedding": embedding,
        }
        await content_model.save(data)
    print("Import task completed")

@router.post("/knowledgecontent_upload")
@login_required
async def knowledgecontent_upload(request: Request,file: UploadFile = File(...)):
    try:
        # 使用相对路径指定上传文件夹
        upload_folder = "upload"
        os.makedirs(upload_folder, exist_ok=True)  # 确保目标文件夹存在
        file_path = os.path.join(upload_folder, file.filename)

        # 保存文件到相对路径
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


        return ResponseModel(code=0, msg=file_path)
    except Exception as e:
        return ResponseModel(code=1, msg=f"文件处理失败：{str(e)}")


# 知识库内容 - 搜索
@router.post("/knowledgecontent/search")
@login_required
async def knowledgecontent_search(
    request: Request,
    page: int = Form(1),
    limit: int = Form(10),
    base_id: Optional[str] = Form(None),
    keyword: Optional[str] = Form(None),
):
    model = KnowledgeContentModel()
    conditions = {}
    if base_id:
        base_id = int(base_id)
        conditions['base_id'] = base_id
    if keyword:
        conditions["content"] = f"%{keyword}%"  # 支持模糊查询
    paginated_data = await model.get_paginated(page=page, per_page=limit, conditions=conditions)
    return ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],
        count=paginated_data["total"]
    )

# 知识库内容 - 保存
@router.post("/knowledgecontent/save")
@login_required
async def knowledgecontent_save(request: Request):
    form_data = await request.form()
    model = KnowledgeContentModel()
    knowledegebase_model = KnowledgeBaseModel()
    content_id = form_data.get("id")
    if content_id:
        content_id = int(content_id)
    base_id = int(form_data.get("base_id"))
    embedding_model = await knowledegebase_model.get_model_details_by_base_id(base_id)
    if not embedding_model:
        return ResponseModel(code=1, msg="模型配置错误")

    content = form_data.get("content")
    aiApi = ai(embedding_model['api_key'],embedding_model['base_url'])
    embedding = await aiApi.embedding(embedding_model['model'],content)
    if content_id:
        data = {"base_id": base_id, "content": content,
            "embedding": list_to_vector(embedding),
            "created_at": datetime.now()}
        model.update(content_id, data)
        msg = "知识库内容更新成功"
    else:
        data = {"base_id": base_id, "content": content,
            "embedding": list_to_vector(embedding),
            "created_at": datetime.now()}
        await model.save(data)
        msg = "知识库内容创建成功"

    return ResponseModel(code=0, msg=msg)

# 知识库内容 - 删除
@router.post("/knowledgecontent/del")
@login_required
async def knowledgecontent_del(request: Request):
    form_data = await request.form()
    content_id = form_data.get("id")
    model = KnowledgeContentModel()

    if content_id:
        await model.delete(int(content_id))
        return ResponseModel(code=0, msg="知识库内容删除成功")
    return ResponseModel(code=1, msg="内容 ID 不能为空")

# 批量删除
@router.post("/knowledgecontent/del_batch")
@login_required
async def batch_del(request: Request):
    form_data = await request.form()
    ids = form_data.getlist("ids[]")
    model = KnowledgeContentModel()
    if ids:
        ids = [int(id) for id in ids]
        await model.batch_delete(ids)
        return ResponseModel(
            code=0,
            msg="批量删除成功"
        )
    return ResponseModel(
        code=1,
        msg="ID 不能为空"
    )