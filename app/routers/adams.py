"""
app/routers/adams.py
====================
FastAPI router for the Adams-Bashforth ODE solver API.

Endpoint:
    POST /api/adams/compute
"""

from fastapi import APIRouter, HTTPException
from app.schemas  import AdamsRequest, AdamsResponse, ErrorResponse
from app.numerics import adams_bashforth

router = APIRouter()


@router.post(
    "/compute",
    response_model=AdamsResponse,
    summary="Run Adams-Bashforth Method",
    description=(
        "Solves dy/dx = f(x, y) using the explicit Adams-Bashforth multi-step method "
        "(AB-2 or AB-4). Startup values are computed automatically via RK4."
    ),
    responses={
        200: {"description": "ODE solved successfully.", "model": AdamsResponse},
        400: {"description": "Invalid input or expression.", "model": ErrorResponse},
    },
)
async def compute_adams(body: AdamsRequest):
    """
    **Adams-Bashforth Method** — ODE solver.

    - **func**  : dy/dx expression in x and y  e.g. `x + y`, `-2*y`
    - **order** : 2 for AB-2, 4 for AB-4
    - **x0**    : initial x value
    - **y0**    : initial y(x₀) value
    - **h**     : step size (must be > 0)
    - **steps** : number of steps to compute (4–500)

    The required startup values are bootstrapped automatically using
    4th-order Runge-Kutta (RK4), so no manual startup is needed.
    """
    try:
        result = adams_bashforth(
            func_str = body.func,
            order    = body.order,
            x0       = body.x0,
            y0       = body.y0,
            h        = body.h,
            steps    = body.steps,
        )
        return {"ok": True, **result}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal error: {exc}")