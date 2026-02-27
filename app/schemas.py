"""
app/schemas.py
==============
Pydantic v2 models for all API request bodies and response shapes.
FastAPI uses these automatically for validation and OpenAPI docs.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


# ══════════════════════════════════════════════════════════════════════════════
#  POWER METHOD
# ══════════════════════════════════════════════════════════════════════════════

class PowerRequest(BaseModel):
    """POST /api/power/compute — request body."""

    matrix: list[list[float]] = Field(
        ...,
        description="n×n square matrix as a list of rows.",
        examples=[[[4, 1, 2], [1, 3, 0], [2, 0, 5]]]
    )
    tol: float = Field(
        default=1e-6,
        gt=0,
        description="Convergence tolerance (must be > 0).",
        examples=[0.0001]
    )
    max_iter: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum number of iterations (1–1000).",
        examples=[100]
    )

    @field_validator("matrix")
    @classmethod
    def validate_matrix(cls, m):
        n = len(m)
        if n < 2 or n > 10:
            raise ValueError("Matrix size must be between 2×2 and 10×10.")
        for i, row in enumerate(m):
            if len(row) != n:
                raise ValueError(
                    f"Row {i+1} has {len(row)} elements but expected {n} (matrix must be square)."
                )
        return m


class IterationEntry(BaseModel):
    iter:   int
    lambda_: float = Field(alias="lambda")
    error:  Optional[str]
    norm:   float

    class Config:
        populate_by_name = True


class PowerResponse(BaseModel):
    """POST /api/power/compute — response body."""
    ok:          bool
    eigenvalue:  float
    eigenvector: list[float]
    iterations:  int
    converged:   bool
    log:         list[dict]


# ══════════════════════════════════════════════════════════════════════════════
#  SIMPSON'S 1/3 RULE
# ══════════════════════════════════════════════════════════════════════════════

class SimpsonsRequest(BaseModel):
    """POST /api/simpsons/compute — request body."""

    func: str = Field(
        ...,
        description="Math expression in x. e.g. 'sin(x)', 'x**2', 'exp(-x)'.",
        examples=["sin(x)"]
    )
    a: float = Field(..., description="Lower integration limit.",   examples=[0.0])
    b: float = Field(..., description="Upper integration limit.",   examples=[3.14159265])
    n: int   = Field(
        ...,
        ge=2,
        le=10000,
        description="Number of sub-intervals (must be even, ≥ 2).",
        examples=[10]
    )

    @field_validator("b")
    @classmethod
    def b_gt_a(cls, b, info):
        a = info.data.get("a")
        if a is not None and b <= a:
            raise ValueError("Upper limit b must be greater than lower limit a.")
        return b


class QuadraturePoint(BaseModel):
    i:            int
    x:            float
    fx:           float
    weight:       int
    contribution: float


class SimpsonsResponse(BaseModel):
    """POST /api/simpsons/compute — response body."""
    ok:       bool
    integral: float
    h:        float
    n:        int
    points:   list[dict]


# ══════════════════════════════════════════════════════════════════════════════
#  ADAMS-BASHFORTH
# ══════════════════════════════════════════════════════════════════════════════

class AdamsRequest(BaseModel):
    """POST /api/adams/compute — request body."""

    func: str = Field(
        ...,
        description="dy/dx expression in x and y. e.g. 'x + y', '-2*y'.",
        examples=["x + y"]
    )
    order: int = Field(
        default=4,
        description="Method order: 2 for AB-2, 4 for AB-4.",
        examples=[4]
    )
    x0:    float = Field(..., description="Initial x value.",         examples=[0.0])
    y0:    float = Field(..., description="Initial y(x₀) value.",     examples=[1.0])
    h:     float = Field(..., gt=0, description="Step size (> 0).",   examples=[0.1])
    steps: int   = Field(
        ...,
        ge=4,
        le=500,
        description="Number of steps to compute (4–500).",
        examples=[10]
    )

    @field_validator("order")
    @classmethod
    def order_valid(cls, v):
        if v not in (2, 4):
            raise ValueError("Order must be 2 (AB-2) or 4 (AB-4).")
        return v


class SolutionRow(BaseModel):
    step:   int
    x:      float
    y:      float
    f:      float
    method: str


class AdamsResponse(BaseModel):
    """POST /api/adams/compute — response body."""
    ok:      bool
    final_x: float
    final_y: float
    method:  str
    startup: int
    rows:    list[dict]


# ══════════════════════════════════════════════════════════════════════════════
#  GENERIC ERROR RESPONSE
# ══════════════════════════════════════════════════════════════════════════════

class ErrorResponse(BaseModel):
    ok:    bool = False
    error: str