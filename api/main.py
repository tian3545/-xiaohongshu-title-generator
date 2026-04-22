from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(__file__))

from config.settings import settings
from database import init_db
from api.routers import auth, content, payment, user

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="小红书爆款文案生成器 - 按次付费模式"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
static_dir = os.path.join(os.path.dirname(__file__), "web", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 注册路由
app.include_router(auth.router)
app.include_router(content.router)
app.include_router(payment.router)
app.include_router(user.router)

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

# 根路径返回首页
@app.get("/")
async def root():
    """返回首页"""
    index_path = os.path.join(os.path.dirname(__file__), "web", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "小红书文案生成器 API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    # 初始化数据库
    init_db()
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 启动成功！")
    print(f"📚 API文档: http://localhost:{settings.PORT}/docs")

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print(f"👋 {settings.APP_NAME} 已关闭")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
