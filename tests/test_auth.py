import pytest
from itsdangerous import URLSafeTimedSerializer

from src.config import settings
from src.features.auth.security import (
    SESSION_COOKIE_NAME,
    create_session_token,
    is_authenticated,
    verify_password,
    create_login_response,
    create_logout_response,
)


# ===== verify_password =====

class TestVerifyPassword:
    def test_correct_password(self):
        assert verify_password("test-password") is True

    def test_wrong_password(self):
        assert verify_password("wrong") is False

    def test_empty_password_raises_if_not_configured(self, monkeypatch):
        monkeypatch.setattr(settings, "echo_password", "")
        with pytest.raises(RuntimeError, match="ECHO_PASSWORD"):
            verify_password("anything")


# ===== is_authenticated =====

class TestIsAuthenticated:
    def _make_request(self, cookies: dict):
        from starlette.requests import Request
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/",
            "headers": [],
            "query_string": b"",
        }
        request = Request(scope)
        request._cookies = cookies
        return request

    def test_valid_token_returns_true(self):
        token = create_session_token()
        request = self._make_request({SESSION_COOKIE_NAME: token})
        assert is_authenticated(request) is True

    def test_no_cookie_returns_false(self):
        request = self._make_request({})
        assert is_authenticated(request) is False

    def test_invalid_token_returns_false(self):
        request = self._make_request({SESSION_COOKIE_NAME: "garbage"})
        assert is_authenticated(request) is False

    def test_token_signed_with_wrong_key_returns_false(self):
        bad_serializer = URLSafeTimedSerializer("wrong-key")
        token = bad_serializer.dumps({"authenticated": True})
        request = self._make_request({SESSION_COOKIE_NAME: token})
        assert is_authenticated(request) is False

    def test_secret_key_not_configured_raises(self, monkeypatch):
        monkeypatch.setattr(settings, "session_secret_key", "")
        token = "anything"
        request = self._make_request({SESSION_COOKIE_NAME: token})
        with pytest.raises(RuntimeError, match="SESSION_SECRET_KEY"):
            is_authenticated(request)


# ===== create_login_response =====

class TestCreateLoginResponse:
    def test_redirects_to_next_url(self):
        response = create_login_response("/milestones/test")
        assert response.status_code == 303
        assert response.headers["location"] == "/milestones/test"

    def test_redirects_to_root_when_next_is_empty(self):
        response = create_login_response("")
        assert response.headers["location"] == "/"

    def test_sets_session_cookie(self):
        response = create_login_response("/")
        cookie_header = response.headers.get("set-cookie", "")
        assert SESSION_COOKIE_NAME in cookie_header

    def test_cookie_is_httponly(self):
        response = create_login_response("/")
        assert "httponly" in response.headers["set-cookie"].lower()


# ===== create_logout_response =====

class TestCreateLogoutResponse:
    def test_redirects_to_login(self):
        response = create_logout_response()
        assert response.status_code == 303
        assert response.headers["location"] == "/login"

    def test_deletes_session_cookie(self):
        response = create_logout_response()
        cookie_header = response.headers.get("set-cookie", "")
        assert SESSION_COOKIE_NAME in cookie_header
        assert 'max-age=0' in cookie_header.lower() or 'expires=' in cookie_header.lower()
