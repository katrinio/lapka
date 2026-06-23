from src.milestones.tags import parse_tags


def test_parse_tags_splits_by_spaces_and_commas():
    assert parse_tags("vpn, infra friends") == ["FRIENDS", "INFRA", "VPN"]


def test_parse_tags_removes_duplicates():
    assert parse_tags("vpn vpn infra") == ["INFRA", "VPN"]


def test_parse_tags_handles_empty_string():
    assert parse_tags("") == []