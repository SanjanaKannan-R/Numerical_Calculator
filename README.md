# 🔢 NumerIQ — Numerical Methods Web Calculator

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

*NumerIQ* is a high-fidelity numerical analysis web application built with *FastAPI*. It bridges the gap between complex mathematical theory and interactive visualization, allowing users to run classic algorithms directly in the browser with full step-by-step transparency.

Instead of "black-box" computations found in MATLAB or Excel, NumerIQ exposes the *mechanics of convergence*, providing detailed iteration tables and error tracking.

---

## 🌟 Key Features

### ⚡ Eigenvalue Discovery (Power Method)
Find the dominant eigenvalue and its corresponding eigenvector for square matrices (2×2 to 5×5).
* *Precision Control:* Custom tolerance and max-iteration settings.
* *Transparency:* Full convergence history showing the refinement of $\lambda$ at every step.

### 📐 Definite Integration (Simpson’s 1/3 Rule)
Evaluate integrals of complex mathematical expressions with high accuracy.
* *Smart Parsing:* Handles standard math notation (e.g., sin(x), e^x, sqrt(x)).
* *Quadrature Insights:* Displays a breakdown of weights and interval points.

### 📊 ODE Solvers (Adams–Bashforth AB-2 & AB-4)
Solve first-order Ordinary Differential Equations ($dy/dx = f(x, y)$) using multi-step methods.
* *Hybrid Approach:* Utilizes an *RK4 (Runge-Kutta 4)* "startup" phase to generate initial values automatically.
* *Color-Coded Analysis:* Tables clearly distinguish between startup values and multi-step predictions.

---

## 🏗 Technical Architecture

NumerIQ is built on a *Clean Architecture* pattern, ensuring that the mathematical logic is decoupled from the web framework.

* *Backend:* FastAPI for high-performance asynchronous request handling.
* *Validation:* Pydantic schemas for strict input sanitization and error reporting.
* *Pure Logic:* Algorithms are implemented in *Vanilla Python*. No NumPy or SciPy—purely to demonstrate algorithmic mastery.
* *Frontend:* Jinja2 templates styled with modern CSS for a responsive, clean UI.

### 📂 Project Structure
```text
numeriq_fastapi/
├── app/
│   ├── numerics.py    # The "Brain": Core algorithm implementations
│   ├── schemas.py     # The "Gatekeeper": Pydantic data validation models
│   ├── routers/       # The "Traffic Controller": API endpoint logic
│   └── templates/     # The "Face": HTML & CSS frontend
├── main.py            # Entry point
└── requirements.txt
---
###🚀 Getting Started
To get the project running locally, follow these steps:

Bash
# 1. Clone the repository
git clone <your-repo-url>
cd numeriq_fastapi

# 2. Create and activate a virtual environment (Recommended)
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Launch the FastAPI development server
uvicorn main:app --reload

# 5. Access the application
# Web UI: [http://127.0.0.1:8000](http://127.0.0.1:8000)
# API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


