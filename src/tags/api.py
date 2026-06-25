import logging

from fastapi import APIRouter, HTTPException, Request

from src.milestones.services import group_by_day
from src.orm.tag import Tag
from src.web.templates import templates

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/tags/{tag_name}")
def tag_page(request: Request, tag_name: str):
    logger.debug("Requested tag page for tag_name=%s", tag_name)
    tag = Tag.get_by_name(tag_name.upper())
    if tag is None:
        logger.debug("Tag not found for tag_name=%s", tag_name)
        raise HTTPException(status_code=404, detail="Tag not found")

    milestones = list(tag.milestones)
    logger.debug(
        "Tag found for tag_name=%s milestone_count=%s", tag_name, len(milestones)
    )

    return templates.TemplateResponse(
        request,
        "tags/tag.html",
        {
            "tag": tag,
            "grouped_milestones": group_by_day(milestones),
        },
    )

@router.get("/tags")
def tags_page(request: Request):
    return templates.TemplateResponse(
        request,
        "tags/tags.html",
        {
            "tags": Tag.all_with_counts(),
        },
    )
