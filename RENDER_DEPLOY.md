## Render deployment

This project is ready to deploy to Render as a Python web service.

### Included files

- `render.yaml` for Render Blueprint setup
- `.python-version` to pin the Python version
- `/healthz` endpoint for Render health checks

### How to deploy

1. Push this project to GitHub or GitLab.
2. In Render, choose `New +` -> `Blueprint`.
3. Connect the repository.
4. Render will detect `render.yaml` and create the web service.
5. Once deployment finishes, open the generated service URL.

### Manual service settings

If you prefer to create the service manually instead of using the Blueprint:

- Environment: `Python`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/healthz`
