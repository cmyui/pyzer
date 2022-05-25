import asyncio
import json
import secrets
import time
from typing import Literal

import bcrypt
from fastapi import APIRouter
from fastapi import Form
from fastapi import HTTPException
from fastapi import status

from pyzer import models
from pyzer import services
from pyzer import settings

router = APIRouter(prefix="/oauth")


@router.post("/token")
async def oauth_token(
    username: str = Form(...),
    password: str = Form(...),
    grant_type: Literal["password"] = Form(...),  # TODO: others
    client_id: int = Form(...),
    client_secret: str = Form(..., min_length=40, max_length=40),
    scope: Literal["*"] = Form(...),  # TODO: others
):
    # identify osu!lazer client
    assert client_id == 5
    assert client_secret == "FGc9GAtyHzeQDshWP5Ah7dega8hJACAJpQtw6OXk"

    # validate credentials
    row = await services.database.fetch_one(
        "SELECT id, hashed_password FROM users WHERE username = :username",
        {"username": username},
    )

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None,  # default executor
        bcrypt.checkpw,
        password.encode(),
        row["hashed_password"].encode(),
    )
    if not result:
        print(
            "\x1b[;91m",
            f"Invalid credentials for user",
            username,
            "\x1b[m",
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                # TODO: check how osu! generally does these
                "error": "invalid credentials",
                "hint": "Check your username and password",
                "message": "Invalid credentials",
            },
        )

    # create new session

    print(
        "\x1b[;92m",
        "Creating new session for user",
        username,
        "\x1b[m",
    )

    session: models.Session = {
        "token_type": "Bearer",
        "access_token_expiry": time.time() + settings.ACCESS_TOKEN_EXPIRATION_SECONDS,
        "access_token": secrets.token_urlsafe(16),
        "refresh_token": secrets.token_urlsafe(16),  # TODO: is this even used?
        "id": row["id"],
        "username": username,
    }

    await services.redis_sessions_db.setex(
        name=session["access_token"],
        time=settings.ACCESS_TOKEN_EXPIRATION_SECONDS,
        value=json.dumps(session),
    )

    resp = {
        "token_type": session["token_type"],
        "expires_in": int(session["access_token_expiry"] - time.time()),
        "access_token": session["access_token"],
        "refresh_token": session["refresh_token"],
    }

    return resp
