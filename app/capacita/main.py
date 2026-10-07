from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from capacita.database import engine
from capacita.models import Base
from capacita.routers.employee_router import router as employee_router
from capacita.routers.health_router import router as health_router
from capacita.settings import settings


TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Capacita - Backend Capacity Planner API", lifespan=lifespan)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


app.include_router(employee_router)
app.include_router(health_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("capacita.main:app", host=settings.host, port=settings.port, reload=False)

