# auth/auth_middleware.py

from fastapi import Header, HTTPException
from auth.jwt_handler import verify_access_token


async def auth_user(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        scheme, token = Authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token scheme")
    except:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload  # will have {admin_id, organization}
