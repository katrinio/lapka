import re

_SPLIT_RE = re.compile(r"[,\s]+")
_TAG_RE = re.compile(r"^[A-Z0-9_]{1,32}$")


def slug_from_title(title: str) -> str:
    slug = title.strip().upper()
    slug = re.sub(r"[^A-Z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug)
    return slug.strip("_")


def slug_with_suffix(base_slug: str, suffix: int) -> str:
    if suffix <= 1:
        return base_slug
    return f"{base_slug}_{suffix}"


def normalize_tag(raw_tag: str) -> str:
    tag = raw_tag.strip().upper()
    if not tag:
        raise ValueError("Tag must not be empty.")
    if not _TAG_RE.fullmatch(tag):
        raise ValueError(
            f"Invalid tag: {raw_tag!r}. Use only A-Z, 0-9 and underscore, up to 32 characters."
        )
    return tag


def parse_tags(raw_tags: str) -> list[str]:
    parts = _SPLIT_RE.split(raw_tags.strip())
    normalized = {normalize_tag(part) for part in parts if part.strip()}
    return sorted(normalized)
