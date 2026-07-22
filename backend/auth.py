import os
from functools import lru_cache
from typing import Any

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer_scheme = HTTPBearer(auto_error=False)


class AuthConfigurationError(RuntimeError):
    """Raised when Cognito auth is enabled but not correctly configured."""


class InvalidAuthToken(ValueError):
    """Raised when a bearer token doesn't validate as a Cognito access token."""


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def cognito_auth_enabled() -> bool:
    explicit = os.environ.get("COGNITO_AUTH_ENABLED")
    if explicit is not None:
        return _env_bool("COGNITO_AUTH_ENABLED")
    return bool(
        os.environ.get("COGNITO_USER_POOL_ID")
        and os.environ.get("COGNITO_APP_CLIENT_ID")
    )


def _user_pool_id() -> str:
    return os.environ.get("COGNITO_USER_POOL_ID", "").strip()


def _app_client_id() -> str:
    return os.environ.get("COGNITO_APP_CLIENT_ID", "").strip()


def _region() -> str:
    configured_region = os.environ.get("COGNITO_REGION", "").strip()
    if configured_region:
        return configured_region

    user_pool_id = _user_pool_id()
    if "_" in user_pool_id:
        return user_pool_id.split("_", 1)[0]

    return ""


def cognito_issuer() -> str:
    region = _region()
    user_pool_id = _user_pool_id()
    if not region or not user_pool_id:
        raise AuthConfigurationError(
            "Cognito auth requires COGNITO_REGION, "
            "COGNITO_USER_POOL_ID, and COGNITO_APP_CLIENT_ID."
        )
    return f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"


@lru_cache(maxsize=4)
def _jwks_client(issuer: str) -> Any:
    _, pyjwk_client = _jwt_tools()
    return pyjwk_client(f"{issuer}/.well-known/jwks.json")


def _jwt_tools() -> tuple[Any, Any]:
    try:
        import jwt
        from jwt import PyJWKClient
    except ImportError as exc:
        raise AuthConfigurationError(
            "Cognito auth requires PyJWT. Install backend requirements."
        ) from exc
    return jwt, PyJWKClient


def verify_cognito_access_token(token: str) -> dict[str, Any]:
    client_id = _app_client_id()
    if not client_id:
        raise AuthConfigurationError(
            "Cognito auth requires COGNITO_APP_CLIENT_ID."
        )

    issuer = cognito_issuer()
    jwt, _ = _jwt_tools()
    try:
        signing_key = _jwks_client(issuer).get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=issuer,
            options={"verify_aud": False},
        )

        if claims.get("token_use") != "access":
            raise jwt.InvalidTokenError("Expected a Cognito access token.")

        if claims.get("client_id") != client_id:
            raise jwt.InvalidTokenError("Token client_id does not match.")
    except jwt.PyJWTError as exc:
        raise InvalidAuthToken("Invalid authentication token.") from exc

    return claims


async def require_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
) -> dict[str, Any]:
    if not cognito_auth_enabled():
        return {"sub": "local-dev", "auth_disabled": True}

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return verify_cognito_access_token(credentials.credentials)
    except AuthConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except InvalidAuthToken as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
