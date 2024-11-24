from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

test_router = APIRouter()


@test_router.get("/")
async def main():
    """
    返回包含 HTML 表单的页面，用户可以通过此页面上传文件。
    """
    content = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>文件上传示例</title>
      <!-- 请勿在项目正式环境中引用该 layui.css 地址 -->
      <link href="//unpkg.com/layui@2.9.18/dist/css/layui.css" rel="stylesheet">
    </head>
    <body>
    <div class="layui-upload-drag" id="ID-upload-demo-drag">
      <i class="layui-icon layui-icon-upload"></i> 
      <div>点击上传，或将文件拖拽到此处</div>
      <div class="layui-hide" id="ID-upload-demo-preview">
        <hr> <img src="" alt="上传成功后渲染" style="max-width: 100%">
      </div>
    </div>
      
    <!-- 请勿在项目正式环境中引用该 layui.js 地址 -->
    <script src="//unpkg.com/layui@2.9.18/dist/layui.js"></script>
    <script>
    layui.use(function(){
      var upload = layui.upload;
      var $ = layui.$;
      // 渲染 LayUI 上传组件
      upload.render({
        elem: '#ID-upload-demo-drag', // 绑定上传按钮
        url: '/test/upload',         // 后端文件上传接口
        accept: 'file',              // 支持所有文件类型
        done: function(res){
          // 上传完成后的回调
          if (res.filename) {
            layer.msg('上传成功：' + res.filename);
            $('#ID-upload-demo-preview').removeClass('layui-hide')
              .find('img').attr('src', res.filename); // 渲染预览
          } else {
            layer.msg('上传失败：' + (res.message || '未知错误'));
          }
        },
        error: function(){
          // 上传失败的回调
          layer.msg('上传失败，请重试');
        }
      });
    });
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=content)


@test_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    处理文件上传并返回文件相关信息
    """
    try:
        # 读取文件内容
        file_content = await file.read()
        if not file_content:
            return JSONResponse(content={"message": "文件内容为空"}, status_code=400)
        
        # 返回文件元数据
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size": len(file_content)
        }
    except Exception as e:
        return {"error": str(e)}
