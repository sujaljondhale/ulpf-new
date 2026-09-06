from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api.routes import router as api_router, syslog_collector, file_collector, ingestion_queue
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start background queue and log collectors
    ingestion_queue.start()
    syslog_collector.start()
    file_collector.start()
    yield
    # Shutdown: Gracefully stop background collectors and queue
    syslog_collector.stop()
    file_collector.stop()
    ingestion_queue.stop()


app = FastAPI(
    title=settings.app_name,
    description="Universal Log Pre-processing Framework (ULPF) — SIH Problem SIH 26156 Master Implementation",
    version=settings.version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def read_root():
    return RedirectResponse(url="/dashboard/")


@app.get("/client")
def read_client():
    return RedirectResponse(url="/dashboard/client_app.html")


# Mount Web Dashboard static directory if present
dashboard_dir = Path(__file__).parent.parent / "dashboard"
if dashboard_dir.exists():
    app.mount("/dashboard", StaticFiles(directory=str(dashboard_dir), html=True), name="dashboard")
