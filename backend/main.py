# ============================================================
# 颐邻通 V1.0 - FastAPI 入口
# 一体化服务：同时提供 /api/* 接口 + /static/* 前端静态资源
# 启动：python main.py  然后浏览器打开 http://localhost:8000/login.html
# ============================================================

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from routers import auth, orders

# ----------- 1. 建表 -----------
Base.metadata.create_all(bind=engine)

# ----------- 2. 创建 FastAPI 应用 -----------
app = FastAPI(
    title="颐邻通 V1.0 · 社区养老便民服务平台 API",
    version="1.0.0",
    description="V1.0 首期工程：登录 + 咨询工单全流程",
)

# ----------- 3. 跨域配置（CORS） -----------
# 开发阶段允许所有来源，生产环境应收紧到具体域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],       # 允许所有 HTTP 方法
    allow_headers=["*"],       # 允许所有请求头
)

# ----------- 4. 注册路由 -----------
app.include_router(auth.router,  prefix="/api", tags=["登录"])
app.include_router(orders.router, prefix="/api", tags=["工单"])

# ----------- 5. 托管前端静态资源 -----------
# frontend/ 目录下的 HTML/CSS/JS 直接通过浏览器访问
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


# ----------- 6. 根路径 -----------
@app.get("/api", tags=["系统"])
def api_root():
    return {
        "message": "颐邻通 V1.0 API 已启动",
        "docs": "/docs",
        "frontend": "/login.html",
    }


# ----------- 7. 直接运行 -----------
if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("  颐邻通 V1.0 社区养老便民服务平台")
    print("  后端 API：  http://localhost:8000/docs")
    print("  前端首页：  http://localhost:8000/login.html")
    print("=" * 60)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
