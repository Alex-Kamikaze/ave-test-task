from fastapi import FastAPI
import uvicorn
from app.api.views.views import router as views_router
from app.core.settings import settings

app = FastAPI()
app.include_router(views_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug)
