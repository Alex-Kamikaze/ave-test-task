from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.views.views import router as views_router
from app.config.settings import settings
from app.metrics.api_metrics import total_keys_in_application

app = FastAPI()
app.include_router(views_router, prefix="/api")

instrumentator = Instrumentator().instrument(app)
instrumentator.add(total_keys_in_application()).expose(app)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="debug")
