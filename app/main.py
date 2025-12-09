from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.database import Base, engine
from app.routers import auth_router, config_router, analysis_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Kubernetes Resource Analysis API",
    description="AI-powered Kubernetes resource optimization tool",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(config_router)
app.include_router(analysis_router)

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Mount static files (if needed)
# app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Dashboard page"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "username": "User"
    })


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Register page"""
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/logout")
async def logout():
    """Logout endpoint"""
    return RedirectResponse(url="/login")


@app.get("/configurations", response_class=HTMLResponse)
async def configurations_page(request: Request):
    """Configurations list page"""
    return templates.TemplateResponse("configurations.html", {
        "request": request,
        "username": "User"
    })


@app.get("/configurations/new", response_class=HTMLResponse)
async def config_form_page(request: Request):
    """Configuration form page"""
    return templates.TemplateResponse("config_form.html", {
        "request": request,
        "username": "User"
    })


@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    """Analysis page"""
    return templates.TemplateResponse("analysis.html", {
        "request": request,
        "username": "User"
    })


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Service is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
