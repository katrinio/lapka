from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.orm.tag import Tag
from src.tags.services import get_milestones_for_tag

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


@router.get("/tags/{tag}")
def tag_page(request: Request, tag: str):
    return templates.TemplateResponse(
        request,
        "milestones/tag.html",
        {
            "tag": Tag.get_by_name(tag.upper()),
            "milestones": get_milestones_for_tag(tag),
        },
    )
