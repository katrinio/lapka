from fastapi import APIRouter, Request

from src.features.terminal.commands import COMMANDS
from src.web.templates import templates

router = APIRouter()


@router.get("/help")
def help_page(request: Request):
    return templates.TemplateResponse(
        request,
        "terminal/help.html",
        {"commands": COMMANDS},
    )
