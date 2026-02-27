"""
main.py  —  NumerIQ FastAPI Application
========================================
Entry point for the NumerIQ numerical methods calculator.

Run with:
    uvicorn main:app --reload

Or directly:
    python main.py
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.routers import power, simpsons, adams

# ── App instance ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="NumerIQ — Numerical Methods Calculator",
    description=(
        "A FastAPI-powered web application providing three numerical methods:\n"
        "- Power Method (eigenvalue computation)\n"
        "- Simpson's 1/3 Rule (numerical integration)\n"
        "- Adams-Bashforth Method (ODE solving)"
    ),
    version="1.0.0",
    docs_url="/docs",        # Swagger UI at /docs
    redoc_url="/redoc",      # ReDoc at /redoc
)

# ── CORS middleware — allow all origins for dev ────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Static files (CSS, JS) ─────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ── Jinja2 templates ───────────────────────────────────────────────────────────
templates = Jinja2Templates(directory="app/templates")

# ── Include API routers ────────────────────────────────────────────────────────
app.include_router(power.router,    prefix="/api/power",    tags=["Power Method"])
app.include_router(simpsons.router, prefix="/api/simpsons", tags=["Simpson's Rule"])
app.include_router(adams.router,    prefix="/api/adams",    tags=["Adams-Bashforth"])

# ── Page routes ────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    """Render the home / launcher page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/power", response_class=HTMLResponse, include_in_schema=False)
async def page_power(request: Request):
    """Render the Power Method calculator page."""
    return templates.TemplateResponse("power.html", {"request": request})


@app.get("/simpsons", response_class=HTMLResponse, include_in_schema=False)
async def page_simpsons(request: Request):
    """Render the Simpson's 1/3 Rule calculator page."""
    return templates.TemplateResponse("simpsons.html", {"request": request})


@app.get("/adams", response_class=HTMLResponse, include_in_schema=False)
async def page_adams(request: Request):
    """Render the Adams-Bashforth calculator page."""
    return templates.TemplateResponse("adams.html", {"request": request})


# ── Dev server entry point ─────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)