from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.event_manager import EventManager
from app.api.routes import router
import os

# Get the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="Azure Event Grid Viewer")
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# Initialize event manager
event_manager = EventManager()

# Include routes
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
async def startup_event():
    """Application initialization on startup"""
    pass

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup work on application shutdown"""
    await event_manager.close()