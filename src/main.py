from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.routes import router
from src.errors.handlers import register_exception_handlers


@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is starting.....")
    await init_db()
    yield
    print("server has been stopped")


version = "v1"
version_prefix = f"/api/{version}"
app = FastAPI(
    title="String Analyzer Service API",
    description="A REST API service that analyzes strings and stores their computed properties",
    version=version,
    contact={"email": "tonycypher0@gmail.com"},
    openapi_url=f"{version_prefix}/openapi.json",
    lifespan=life_span,
)

register_exception_handlers(app)

app.include_router(router, prefix="/strings", tags=["String Analyzer"])


@app.get("/")
async def read_root():
    return {"message": "Hello world"}
