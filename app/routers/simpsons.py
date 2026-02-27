"""
app/routers/simpsons.py
=======================
FastAPI router for the Simpson's 1/3 Rule API.

Endpoint:
    POST /api/simpsons/compute
"""

from fastapi import APIRouter, HTTPException
from app.schemas  import SimpsonsRequest, SimpsonsResponse, ErrorResponse
from app.numerics import simpsons_rule

router = APIRouter()


@router.post(
    "/compute",
    response_model=SimpsonsResponse,
    summary="Run Simpson's 1/3 Rule",
    description=(
        "Numerically integrates f(x) over [a, b] using parabolic arc approximations. "
        "n is auto-corrected to the nearest even number if needed."
    ),
    responses={
        200: {"description": "Integration succeeded.",   "model": SimpsonsResponse},
        400: {"description": "Invalid input or expression.", "model": ErrorResponse},
    },
)
async def compute_simpsons(body: SimpsonsRequest):
    """
    **Simpson's 1/3 Rule** — numerical integration.

    - **func** : expression in x  e.g. `sin(x)`, `x**2`, `exp(-x)`
    - **a**    : lower limit
    - **b**    : upper limit (must be > a)
    - **n**    : sub-intervals (must be even, ≥ 2)

    Available math functions: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`,
    `abs`, `pow`, `pi`, `e` and all standard `math` functions.
    """
    try:
        result = simpsons_rule(
            func_str = body.func,
            a        = body.a,
            b        = body.b,
            n        = body.n,
        )
        return {"ok": True, **result}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal error: {exc}")