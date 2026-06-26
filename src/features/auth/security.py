import os
import secrets
from datetime import timedelta

from fastapi import Form, Request
from fastapi.responses import RedirectResponse
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


SESSION_COOKIE_NAME = "echo_session"
SESSION_MAX_AGE_SECONDS = int(timedelta(days=30).total_seconds())


def get_session_secret_key() -> str:
    secret_key = os.getenv("SESSION_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SESSION_SECRET_KEY is not configured")
    return secret_key


def get_echo_password() -> str:
    password = os.getenv("ECHO_PASSWORD")
    if not password:
        raise RuntimeError("ECHO_PASSWORD is not configured")
    return password


def get_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(get_session_secret_key())


def create_session_token() -> str:
    return get_serializer().dumps({"authenticated": True})


def is_authenticated(request: Request) -> bool:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return False

    try:
        data = get_serializer().loads(
            token,
            max_age=SESSION_MAX_AGE_SECONDS,
        )
    except (BadSignature, SignatureExpired):
        return False

    return data.get("authenticated") is True


def require_auth(request: Request) -> RedirectResponse | None:
    if is_authenticated(request):
        return None

    return RedirectResponse(
        url=f"/login?next={request.url.path}",
        status_code=303,
    )


def verify_password(password: str) -> bool:
    expected_password = get_echo_password()
    return secrets.compare_digest(password, expected_password)


def create_login_response(next_url: str) -> RedirectResponse:
    response = RedirectResponse(url=next_url or "/", status_code=303)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=create_session_token(),
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response


def create_logout_response() -> RedirectResponse:
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response