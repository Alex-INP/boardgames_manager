from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .config import settings


router = APIRouter()

templates = Jinja2Templates(directory=settings.index_templates_dir)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"name": "username"}
    )
