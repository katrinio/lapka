from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, RedirectResponse

from src.features.terminal.commands import COMMANDS
from src.orm.milestone import Milestone
from src.web.templates import templates

router = APIRouter()


@router.get("/help")
def help_page(request: Request):
    return templates.TemplateResponse(
        request,
        "terminal/help.html",
        {"commands": COMMANDS},
    )


@router.get("/random")
def random_page():
    milestone = Milestone.get_random()
    if milestone is None:
        return PlainTextResponse("No milestones found.")
    return RedirectResponse(url=f"/milestones/{milestone.slug}", status_code=303)
