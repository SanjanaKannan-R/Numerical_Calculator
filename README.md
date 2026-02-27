🔢 NumerIQ — Numerical Methods Web Calculator

A full-stack numerical analysis web app built with FastAPI.
Run classic numerical methods directly in your browser with step-by-step iteration breakdowns.

🌟 Overview

NumerIQ is a web-based numerical methods calculator designed to make classical algorithms interactive, transparent, and easy to experiment with.

Instead of using MATLAB, spreadsheets, or writing scripts, users can:

Enter inputs through a clean UI

Run computations instantly

View detailed iteration tables

Inspect convergence behavior step by step

The project emphasizes algorithm clarity, backend validation, and clean architecture.

🚀 Live Features
⚡ Power Method

Compute the dominant eigenvalue and eigenvector of a square matrix.

Supports 2×2 to 5×5 matrices

Adjustable tolerance

Configurable max iterations

Full convergence history table

Example auto-load option

📐 Simpson’s 1/3 Rule

Numerically evaluate definite integrals.

Accepts custom math expressions

Automatic step-size calculation

Even-interval enforcement

Quadrature point breakdown with weights

Classic sin(x) test example included

📊 Adams–Bashforth Method (AB-2 & AB-4)

Solve first-order ODEs:

dy/dx = f(x, y)

2nd and 4th order implementations

Automatic RK4 startup values

Adjustable step size

Color-coded solution table

Clear separation between RK4 and multi-step phases

🏗 Technical Stack

Backend

FastAPI

Uvicorn

Pydantic (input validation)

Jinja2 (templating)

Architecture

RESTful API design

Modular router structure

Strict schema validation

Pure Python numerical implementations (no NumPy/SciPy)

📂 Project Structure
numeriq_fastapi/
│
├── main.py
├── requirements.txt
├── README.md
│
└── app/
    ├── numerics.py        # Core numerical algorithms
    ├── schemas.py         # API validation models
    ├── routers/           # Endpoint definitions
    └── templates/         # Frontend HTML templates

Clear separation between:

Algorithm logic

API layer

Validation schemas

Presentation layer

▶️ Getting Started
1️⃣ Clone the repository
git clone <your-repo-url>
cd numeriq_fastapi
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the development server
uvicorn main:app --reload
4️⃣ Open in browser
http://127.0.0.1:8000
🔌 API Endpoints
Method	Endpoint
POST	/api/power/compute
POST	/api/simpsons/compute
POST	/api/adams/compute

Interactive API documentation available at:

/docs
🧮 Expression Syntax

Supported examples:

Expression	Input Format

sin
⁡
(
𝑥
)
sin(x)	sin(x)

𝑒
𝑥
e
x
	exp(x)

𝑥
2
x
2
	x**2

𝑥
x
	​

	sqrt(x)

𝜋
π	pi

Safe evaluation — only standard math operations allowed.

🎯 Design Goals

Make numerical methods visually understandable

Demonstrate backend API structuring best practices

Implement classical algorithms without scientific libraries

Maintain clean, readable, academic-grade code

📚 Algorithms Implemented

Power Iteration Method

Simpson’s 1/3 Rule

Adams–Bashforth Multi-Step Methods (AB-2, AB-4)

Runge–Kutta 4 (startup phase)

🧠 Why This Project Stands Out

Algorithms implemented from scratch

Full-stack integration (backend + templated frontend)

Strong validation using Pydantic schemas

Clear separation of concerns

Designed for educational clarity, not black-box computation

🎓 Academic Context

Developed as a university project to explore numerical analysis concepts through real-world implementation. The focus was on understanding algorithm mechanics rather than relying on scientific libraries.
