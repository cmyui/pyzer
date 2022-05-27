from typing import Any
from typing import Mapping

from pyzer import services
from pyzer import settings


async def fetch_all() -> list[Mapping[str, Any]]:
    background_rows = [
        dict(row)  # take mutable copies; we'll need to add more fields
        for row in await services.database.fetch_all(
            "SELECT * FROM seasonal_backgrounds",
        )
    ]

    for background_row in background_rows:
        user_row = await services.database.fetch_one(
            "SELECT id, username, profile_colour, "
            "country_code, is_bot, is_supporter "
            "FROM users WHERE id = :id",
            {"id": background_row["creator_id"]},
        )
        assert user_row is not None

        # add all the user details to the background row
        background_row["user"] = {
            "avatar_url": f"https://a.{settings.DOMAIN}/{user_row['id']}",
            # TODO: these flags
            "is_active": False,
            "is_online": False,
            "is_deleted": False,
            **user_row,
        }

    return background_rows
