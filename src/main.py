from fastapi import FastAPI

version = "v1"
version_prefix = f"/api/{version}"
app = FastAPI(
    title="String Analyzer Service API",
    description="A REST API service that analyzes strings and stores their computed properties",
    version=version,
    contact={"email": "tonycypher0@gmail.com"},
    openapi_url=f"{version_prefix}/openapi.json",
    # lifespan=life_span,
)


@app.get("/")
async def read_root():
    return {"message": "Hello world"}
