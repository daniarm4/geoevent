from fastapi import FastAPI

from src.auth.routers import router as auth_router
from src.event.routers import router as event_router

app = FastAPI(title="Test application")

app.include_router(router=auth_router)
app.include_router(router=event_router)
