# Capacita
FastAPI based team capacity plan backend

## Run project

### Local Development

```bash
uv sync
uv run fastapi dev app/capacita/main.py
```

Or run via module / CLI:
```bash
uv run capacita
```

API docs: `http://127.0.0.1:8000/docs`

## Deploy to Render.com

Render web services require binding to host `0.0.0.0` and the port defined by `$PORT`.

### Configuration (Render Web Service)
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt` (or if using `uv`: `uv sync`)
- **Start Command**: 
  - Recommended: `uv run fastapi run app/capacita/main.py --port $PORT`
  - Or with uvicorn: `uv run uvicorn capacita.main:app --host 0.0.0.0 --port $PORT`
  - Or standard pip: `uvicorn capacita.main:app --host 0.0.0.0 --port $PORT`

> **Note**: Do not use `fastapi dev` in production on Render. `fastapi dev` defaults to `127.0.0.1` instead of `0.0.0.0` and enables file-watch reloaders. Use `fastapi run` which defaults to host `0.0.0.0` and respects `$PORT`.