import json
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from pyzer import models
from pyzer import services

# oauth2: https://tools.ietf.org/id/draft-richer-oauth-json-request-00.html
security = HTTPBearer()


async def authorize_session(
    token: HTTPAuthorizationCredentials = Depends(security),
) -> Optional[models.Session]:
    session = await services.redis_sessions_db.get(token.credentials)
    if session is None:
        return None

    return models.Session(**json.loads(session))
