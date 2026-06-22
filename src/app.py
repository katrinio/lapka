from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

milestones = [
    {
        "title": "VPN for friends",
        "date": "2026-06-22",
        "slug": "VPN_FOR_FRIENDS",
        "description": "Психанула и подняла маленький VPN для друзей.",
    },
    {
        "title": "Domain and SSL",
        "date": "2026-06-21",
        "slug": "DOMAIN_AND_SSL",
        "description": "Подружила сервер с доменом и настроила SSL.",
    },
    {
        "title": "Finpipe v1.0.0",
        "date": "2026-05-27",
        "slug": "FINPIPE_V1_0_0",
        "description": "Первый официальный релиз Finpipe.",
    },
]


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"milestones": milestones},
    )


@app.get("/milestones/{slug}")
def milestone(request: Request, slug: str):
    item = next(m for m in milestones if m["slug"] == slug)
    return templates.TemplateResponse(
        request,
        "milestone.html",
        {"milestone": item},
    )