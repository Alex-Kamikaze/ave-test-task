from fastapi import FastAPI
import uvicorn
from app.api.views.views import router as views_router
from app.config.settings import settings

app = FastAPI()
app.include_router(views_router, prefix="/api")

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="debug")
