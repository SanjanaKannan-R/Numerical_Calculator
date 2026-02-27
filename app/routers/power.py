"""
app/routers/power.py
====================
FastAPI router for the Power Method API.

Endpoint:
    POST /api/power/compute
"""

from fastapi import APIRouter, HTTPException
from app.schemas  import PowerRequest, PowerResponse, ErrorResponse
from app.numerics import power_method

router = APIRouter()


@router.post(
    "/compute",
    response_model=PowerResponse,
    summary="Run Power Method",
    description=(
        "Accepts an n×n matrix and returns the dominant eigenvalue, "
        "normalised eigenvector, and a full iteration log."
    ),
    responses={
        200: {"description": "Computation succeeded.",    "model": PowerResponse},
        400: {"description": "Invalid input or math error.", "model": ErrorResponse},
    },
)
async def compute_power(body: PowerRequest):
    """
    **Power Method** — dominant eigenvalue and eigenvector.

    - **matrix** : n×n list of lists (2×2 to 10×10)
    - **tol**    : convergence tolerance (default 1e-6)
    - **max_iter**: maximum iterations   (default 100)
    """
    try:
        result = power_method(
            A        = body.matrix,
            tol      = body.tol,
            max_iter = body.max_iter,
        )
        return {"ok": True, **result}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal error: {exc}")