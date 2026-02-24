import httpx
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
from shared.auth.jwt import decode_token

router = APIRouter()
security = HTTPBearer(auto_error=False)

# Route map: prefix -> upstream service URL
ROUTE_MAP = {
    "/auth": settings.AUTH_SERVICE_URL,
    "/rbac": settings.RBAC_SERVICE_URL,
    "/quotation": settings.QUOTATION_SERVICE_URL,
    "/invoice": settings.INVOICE_SERVICE_URL,
    "/inventory": settings.INVENTORY_SERVICE_URL,
    "/hris": settings.HRIS_SERVICE_URL,
    "/notifications": settings.NOTIFICATION_SERVICE_URL,
}

# Public routes that don't require JWT
PUBLIC_ROUTES = [
    "/auth/register",
    "/auth/login",
    "/health",
]


def _is_public(path: str) -> bool:
    return any(path.startswith(r) for r in PUBLIC_ROUTES)


def _resolve_upstream(path: str) -> tuple[str, str] | None:
    """Find the upstream URL for a given request path."""
    for prefix, url in ROUTE_MAP.items():
        if path.startswith(prefix):
            return url, path
    return None


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(
    request: Request,
    path: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
):
    full_path = f"/{path}"

    # Health check
    if full_path == "/health":
        return {"status": "healthy", "service": "gateway"}

    # Resolve upstream
    resolved = _resolve_upstream(full_path)
    if not resolved:
        raise HTTPException(status_code=404, detail="Route not found")

    upstream_url, upstream_path = resolved

    # JWT validation for protected routes
    headers = dict(request.headers)
    if not _is_public(full_path):
        if not credentials:
            raise HTTPException(status_code=401, detail="Missing authentication token")
        try:
            token_data = decode_token(credentials.credentials)
            headers["X-User-Id"] = token_data.sub
            headers["X-User-Email"] = token_data.email
            headers["X-User-Roles"] = ",".join(token_data.roles)
            headers["X-User-Permissions"] = ",".join(token_data.permissions)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Remove hop-by-hop headers
    headers.pop("host", None)
    headers.pop("content-length", None)

    # Proxy the request
    body = await request.body()
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.request(
                method=request.method,
                url=f"{upstream_url}{upstream_path}",
                headers=headers,
                content=body,
                params=dict(request.query_params),
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Upstream service unavailable")
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Gateway error: {str(e)}")
