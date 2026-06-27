from pathlib import Path

from fastapi.templating import Jinja2Templates

from src.config import settings

_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=_TEMPLATES_DIR)


def _asset_version(rel_path: str) -> int:
    return int((_TEMPLATES_DIR.parent / "static" / rel_path).stat().st_mtime)


templates.env.globals["asset_version"] = _asset_version
templates.env.globals["settings"] = settings
