import re


def parse_tags(raw_tags: str) -> list[str]:
    parts = re.split(r"[,\s]+", raw_tags.strip())

    return sorted(
        {
            part.upper()
            for part in parts
            if part
        }
    )