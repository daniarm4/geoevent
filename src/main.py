from typing import Annotated

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

from src.dependencies import get_templates
from src.auth.routers import router as auth_router
from src.event.routers import router as event_router

app = FastAPI(title="Test application")

# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/map", response_class=HTMLResponse)
def get_map(request: Request, templates: Annotated[Jinja2Templates, Depends(get_templates)]):
    return templates.TemplateResponse("map.html", {"request": request})


app.include_router(router=auth_router)
app.include_router(router=event_router)
