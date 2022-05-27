from typing import Literal
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from pyzer import models
from pyzer import repositories
from pyzer import services
from pyzer import usecases

router = APIRouter(prefix="/v2")


# @router.get("/users/{value}/{mode}")
async def get_user(
    value: str,
    mode: Optional[Literal["osu", "taiko", "catch", "mania"]] = None,
    key: Optional[Literal["id", "username"]] = Query(None),
):
    if key == "id":
        user = await services.database.fetch_one(
            "SELECT * FROM users WHERE id = :id",
            {"id": int(value)},
        )
    # elif key == "":

    if user is None:
        print(1111, flush=True)
        return  # TODO: what's real err format

    return  # HOW


# NOTE - the trailing `/` matters?
# TODO: is this to differentiate lazer?
@router.get("/me/")
async def get_current_user(
    session: models.Session = Depends(usecases.sessions.authenticate),
):
    user = await repositories.users.fetch_by_id(session.id)
    if user is None:
        print(1111, flush=True)
        return None  # TODO: correct err format

    return user.dict()


@router.get("/friends", response_model=list[int])
async def get_current_friends(
    session: models.Session = Depends(usecases.sessions.authenticate),
):
    return await repositories.users.fetch_friends_by_id(session.id)


@router.get("/seasonal-backgrounds", response_model=models.SeasonalBackgroundsResponse)
async def get_seasonal_backgrounds(
    session: models.Session = Depends(usecases.sessions.authenticate),
):
    background_rows = await repositories.seasonal_backgrounds.fetch_all()

    return {
        "ends_at": "2023-01-01T00:00:00+00:00",
        "backgrounds": background_rows,
    }
