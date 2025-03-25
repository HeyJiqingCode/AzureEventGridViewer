from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.event_manager import EventManager
from app.api.routes import router
import os

# 获取当前目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="Azure Event Grid Viewer")
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# 初始化事件管理器
event_manager = EventManager()

# 包含路由
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
async def startup_event():
    """启动时的应用初始化"""
    pass

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理工作"""
    await event_manager.close()