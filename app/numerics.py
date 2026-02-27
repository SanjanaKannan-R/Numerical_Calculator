"""
app/numerics.py
===============
Pure Python implementations of all three numerical methods.
No external libraries — only the Python standard library (math module).

Exported functions:
    power_method(A, tol, max_iter)            → dict
    simpsons_rule(func_str, a, b, n)          → dict
    adams_bashforth(func_str, order,           → dict
                    x0, y0, h, steps)
"""

import math


# ══════════════════════════════════════════════════════════════════════════════
#  SAFE EXPRESSION EVALUATOR
#  Evaluates a user-supplied math string with variable x (and optionally y).
#  Exposes the full math module so users can write sin(x), exp(x), etc.
# ══════════════════════════════════════════════════════════════════════════════

_SAFE_GLOBALS = {
    "__builtins__": {},          # block all built-ins for safety
    # Trig
    "sin":   math.sin,   "cos":   math.cos,   "tan":   math.tan,
    "asin":  math.asin,  "acos":  math.acos,  "atan":  math.atan,
    "atan2": math.atan2,
    # Exponential / log
    "exp":   math.exp,   "log":   math.log,   "log2":  math.log2,
    "log10": math.log10,
    # Misc
    "sqrt":  math.sqrt,  "abs":   abs,
    "pow":   math.pow,   "ceil":  math.ceil,  "floor": math.floor,
    "round": round,
    # Constants
    "pi":    math.pi,    "e":     math.e,     "inf":   math.inf,
}


def _eval(expr: str, x: float, y: float = 0.0) -> float:
    """
    Safely evaluate a math expression string.
    Variables available: x, y
    Raises ValueError on syntax error or undefined name.
    """
    local_vars = {**_SAFE_GLOBALS, "x": x, "y": y}
    try:
        result = eval(expr, {"__builtins__": {}}, local_vars)  # noqa: S307
        return float(result)
    except ZeroDivisionError:
        raise ValueError(f"Division by zero at x={x}, y={y}.")
    except Exception as exc:
        raise ValueError(
            f"Cannot evaluate '{expr}' at x={x}, y={y}: {exc}"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  METHOD 1 — POWER METHOD
#
#  Purpose : Find the dominant eigenvalue λ₁ and its eigenvector for
#            a real square matrix A.
#
#  Algorithm:
#    1. Start with initial vector x = [1, 1, …, 1]
#    2. Compute  y = A · x            (matrix-vector product)
#    3. Set      λ = ‖y‖∞             (infinity norm ≈ eigenvalue)
#    4. Normalise x = y / λ
#    5. Repeat steps 2-4 until |λ_new − λ_old| < tolerance
# ══════════════════════════════════════════════════════════════════════════════

def _mat_vec(A: list[list[float]], x: list[float]) -> list[float]:
    """Matrix-vector product: returns A · x."""
    return [
        sum(A[i][j] * x[j] for j in range(len(x)))
        for i in range(len(A))
    ]


def _inf_norm(v: list[float]) -> float:
    """Return max(|vᵢ|) — the infinity norm of vector v."""
    return max(abs(vi) for vi in v)


def power_method(
    A:        list[list[float]],
    tol:      float = 1e-6,
    max_iter: int   = 100,
) -> dict:
    """
    Power Method — dominant eigenvalue and eigenvector.

    Parameters
    ----------
    A        : n×n matrix (list of lists of floats)
    tol      : convergence tolerance  (default 1e-6)
    max_iter : maximum iterations     (default 100)

    Returns
    -------
    {
      "eigenvalue"  : float,
      "eigenvector" : list[float],   # normalised, ‖x‖∞ = 1
      "iterations"  : int,
      "converged"   : bool,
      "log"         : list[dict]     # one entry per iteration
    }
    """
    n          = len(A)
    x          = [1.0] * n          # starting vector
    lam        = 0.0
    prev_lam   = 0.0
    converged  = False
    log        = []

    for k in range(1, max_iter + 1):
        y      = _mat_vec(A, x)          # y = A·x
        lam    = _inf_norm(y)            # λ ≈ ‖y‖∞

        if lam == 0.0:
            raise ValueError("Zero vector produced — matrix may be singular.")

        x      = [yi / lam for yi in y]  # normalise
        error  = abs(lam - prev_lam)

        log.append({
            "iter":   k,
            "lambda": round(lam, 10),
            "error":  None if k == 1 else f"{error:.6e}",
            "norm":   round(lam, 8),
        })

        if k > 1 and error < tol:
            converged = True
            break

        prev_lam = lam

    return {
        "eigenvalue":  round(lam, 10),
        "eigenvector": [round(v, 8) for v in x],
        "iterations":  len(log),
        "converged":   converged,
        "log":         log,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  METHOD 2 — SIMPSON'S 1/3 RULE
#
#  Purpose : Numerically integrate f(x) over [a, b].
#
#  Formula :
#    h = (b − a) / n
#    ∫f dx ≈ (h/3)[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + … + 4f(x_{n-1}) + f(xₙ)]
#
#  Weight pattern : 1, 4, 2, 4, 2, …, 4, 1
#  Constraint     : n must be even (auto-corrected if odd)
#  Accuracy       : O(h⁴)
# ══════════════════════════════════════════════════════════════════════════════

def simpsons_rule(
    func_str: str,
    a:        float,
    b:        float,
    n:        int,
) -> dict:
    """
    Simpson's 1/3 Rule — numerical integration.

    Parameters
    ----------
    func_str : expression string in x  e.g. "sin(x)", "x**2"
    a        : lower integration limit
    b        : upper integration limit
    n        : number of sub-intervals (must be ≥ 2; auto-rounded to even)

    Returns
    -------
    {
      "integral" : float,
      "h"        : float,
      "n"        : int,
      "points"   : list[dict]   # quadrature points with weights
    }
    """
    # Enforce even n
    if n % 2 != 0:
        n += 1

    h            = (b - a) / n
    points       = []
    weighted_sum = 0.0

    for i in range(n + 1):
        xi = a + i * h
        fi = _eval(func_str, xi)

        # Simpson weight pattern
        if   i == 0 or i == n: weight = 1
        elif i % 2 != 0:       weight = 4
        else:                   weight = 2

        contribution  = weight * fi
        weighted_sum += contribution

        points.append({
            "i":            i,
            "x":            round(xi, 8),
            "fx":           round(fi, 8),
            "weight":       weight,
            "contribution": round(contribution, 8),
        })

    integral = (h / 3) * weighted_sum

    return {
        "integral": round(integral, 10),
        "h":        round(h, 8),
        "n":        n,
        "points":   points,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  METHOD 3 — ADAMS-BASHFORTH MULTI-STEP METHOD
#
#  Purpose : Solve the initial-value problem  dy/dx = f(x, y),  y(x₀) = y₀.
#
#  Startup : The first `order` values are computed via 4th-order Runge-Kutta
#            because Adams-Bashforth needs prior function values to start.
#
#  AB-2 Formula:
#    y_{n+1} = y_n + (h/2)(3f_n − f_{n-1})
#
#  AB-4 Formula:
#    y_{n+1} = y_n + (h/24)(55f_n − 59f_{n-1} + 37f_{n-2} − 9f_{n-3})
# ══════════════════════════════════════════════════════════════════════════════

def _rk4(
    f: callable,
    x: float,
    y: float,
    h: float,
) -> float:
    """
    4th-order Runge-Kutta single step.
    y_{n+1} = y_n + (h/6)(k₁ + 2k₂ + 2k₃ + k₄)
    """
    k1 = f(x,         y)
    k2 = f(x + h/2,   y + (h/2) * k1)
    k3 = f(x + h/2,   y + (h/2) * k2)
    k4 = f(x + h,     y +  h    * k3)
    return y + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)


def adams_bashforth(
    func_str: str,
    order:    int,
    x0:       float,
    y0:       float,
    h:        float,
    steps:    int,
) -> dict:
    """
    Adams-Bashforth explicit multi-step ODE solver.

    Parameters
    ----------
    func_str : expression string in x, y  e.g. "x + y"
    order    : 2  → AB-2,   4  → AB-4
    x0       : initial x value
    y0       : initial y(x₀) value
    h        : step size (must be > 0)
    steps    : number of steps to compute (must be ≥ 4)

    Returns
    -------
    {
      "final_x" : float,
      "final_y" : float,
      "method"  : str,
      "startup" : int,         # number of RK4 startup points
      "rows"    : list[dict]   # solution table
    }
    """
    f = lambda x, y: _eval(func_str, x, y)  # noqa: E731

    xs      = [x0]
    ys      = [y0]
    fs      = [f(x0, y0)]
    methods = ["Initial"]

    startup = order   # AB-2 needs 2 prior points; AB-4 needs 4

    # ── Phase 1: RK4 startup ──────────────────────────────────────────────────
    for i in range(1, startup):
        if i > steps:
            break
        y_new = _rk4(f, xs[i-1], ys[i-1], h)
        x_new = round(xs[i-1] + h, 12)
        xs.append(x_new)
        ys.append(y_new)
        fs.append(f(x_new, y_new))
        methods.append("RK4 Startup")

    # ── Phase 2: Adams-Bashforth multi-step ───────────────────────────────────
    for i in range(startup, steps + 1):
        if order == 2:
            # AB-2: y_{n+1} = y_n + (h/2)(3f_n − f_{n-1})
            y_new = ys[i-1] + (h / 2) * (3 * fs[i-1] - fs[i-2])

        else:
            # AB-4: y_{n+1} = y_n + (h/24)(55f_n − 59f_{n-1} + 37f_{n-2} − 9f_{n-3})
            y_new = ys[i-1] + (h / 24) * (
                  55 * fs[i-1]
                - 59 * fs[i-2]
                + 37 * fs[i-3]
                -  9 * fs[i-4]
            )

        x_new = round(xs[i-1] + h, 12)
        xs.append(x_new)
        ys.append(y_new)
        fs.append(f(x_new, y_new))
        methods.append(f"AB-{order}")

    # ── Build output rows ─────────────────────────────────────────────────────
    rows = [
        {
            "step":   i,
            "x":      round(xs[i], 6),
            "y":      round(ys[i], 10),
            "f":      round(fs[i], 8),
            "method": methods[i],
        }
        for i in range(len(xs))
    ]

    return {
        "final_x": round(xs[-1], 6),
        "final_y": round(ys[-1], 10),
        "method":  f"AB-{order}",
        "startup": startup,
        "rows":    rows,
    }