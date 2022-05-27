from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from pyzer import models
from pyzer import services
from pyzer import settings
from pyzer import usecases

router = APIRouter(prefix="/v2")


# TODO: figure out what to do about this
def country_code_to_name(country_code: str) -> str:
    return {
        "AU": "Australia",
        "CA": "Canada",
    }[country_code]


# NOTE - the trailing `/` matters?
# TODO: is this to differentiate lazer?
@router.get("/me/")
async def get_current_user(
    session: models.Session = Depends(usecases.sessions.authenticate),
):
    # https://osu.ppy.sh/docs/index.html#user

    # validate credentials
    user_row = await services.database.fetch_one(
        "SELECT * FROM users WHERE id = :id",
        {"id": session["id"]},
    )
    if user_row is None:
        return None  # TODO: what's correct error?

    statistics_row = await services.database.fetch_one(
        "SELECT * FROM user_statistics WHERE id = :id",
        {"id": session["id"]},
    )
    if statistics_row is None:
        return None  # TODO: what's correct error?

    resp = {
        "id": user_row["id"],
        # TODO: customizable subdomains?
        "avatar_url": f"https://a.{settings.DOMAIN}/{user_row['id']}.jpeg",
        "country_code": user_row["country_code"],
        "default_group": "default",  # TODO: whats this?
        "is_active": True,  # TODO: whats this?
        "is_bot": user_row["is_bot"],
        "is_deleted": False,  # TODO: account deletions/deactivations?
        "is_online": True,  # TODO: is this always true when calling this endpoint?
        "is_supporter": user_row["is_supporter"],
        "last_visit": "2020-01-01T00:00:00+00:00",  # TODO
        "pm_friends_only": user_row["pm_friends_only"],
        "profile_colour": user_row["profile_colour"],
        "username": user_row["username"],
        "cover_url": "https://assets.ppy.sh/user-profile-covers/1/0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef.jpeg",  # TODO
        "discord": user_row["discord"],
        "has_supported": user_row["has_supported"],
        "interests": user_row["interests"],  # NOTE: nullable
        "join_date": user_row["join_date"].isoformat(),  # "2010-01-01T00:00:00+00:00",
        "kudosu": {
            "total": user_row["kudosu_total"],
            "available": user_row["kudosu_available"],
        },
        "location": user_row["location"],  # NOTE: nullable
        "max_blocks": user_row["max_blocks"],
        "max_friends": user_row["max_friends"],
        "occupation": user_row["occupation"],  # NOTE: nullable
        "playmode": "osu",  # TODO preference?
        "playstyle": ["mouse", "tablet", "keyboard", "touch"],  # TODO
        "post_count": 0,  # TODO?
        "profile_order": [  # TODO (pg json field?)
            "me",
            "recent_activity",
            "beatmaps",
            "historical",
            "kudosu",
            "top_ranks",
            "medals",
        ],
        "title": user_row["title"],  # TODO
        "twitter": user_row["twitter"],
        "website": user_row["website"],
        "country": {  # TODO, and also why is code duplicated
            "code": user_row["country_code"],
            "name": country_code_to_name(user_row["country_code"]),
        },
        "cover": {  # TODO, and also why is code duplicated
            "custom_url": "https://x.catboy.best/21PPQcH.png",
            "url": "https://x.catboy.best/21PPQcH.png",
            "id": None,
        },
        "is_restricted": False,  # TODO
        "account_history": [],  # TODO: whats this?
        "active_tournament_banner": None,  # TODO
        "badges": [  # TODO
            {
                "awarded_at": "2015-01-01T00:00:00+00:00",
                "description": "Test badge",
                "image_url": "https://assets.ppy.sh/profile-badges/test.png",
                "url": "",
            },
        ],
        "favourite_beatmapset_count": 0,  # TODO
        "follower_count": user_row["follower_count"],
        "graveyard_beatmapset_count": 0,  # TODO
        "groups": [  # TODO
            # {
            #     "id": 1,
            #     "identifier": "gmt",
            #     "name": "gmt",
            #     "short_name": "GMT",
            #     "description": "",
            #     "colour": "#FF0000",
            # }
        ],
        "loved_beatmapset_count": 0,  # TODO
        "monthly_playcounts": [  # TODO
            # {"start_date": "2019-11-01", "count": 100},
            # {"start_date": "2019-12-01", "count": 150},
            # {"start_date": "2020-01-01", "count": 20},
        ],
        "page": {  # TODO
            # "html": "<div class='bbcode bbcode--profile-page'><center>Hello</center></div>",
            # "raw": "[centre]Hello[/centre]",
        },
        "pending_beatmapset_count": 0,  # TODO
        "previous_usernames": [],  # TODO
        "ranked_beatmapset_count": 0,  # TODO
        "replays_watched_counts": [  # TODO
            # {"start_date": "2019-11-01", "count": 10},
            # {"start_date": "2019-12-01", "count": 12},
            # {"start_date": "2020-01-01", "count": 1},
        ],
        "scores_first_count": 0,  # TDOO
        "statistics": {
            # TODO: level calculation based on total score
            "level": {"current": 0, "progress": 0},  # progress 0-100
            # TODO: if score.pp is also an int in the api,
            # then we can just make it int everywhere
            "pp": int(statistics_row["pp"]),
            "global_rank": statistics_row["global_rank"],
            "ranked_score": statistics_row["ranked_score"],
            "hit_accuracy": statistics_row["hit_accuracy"],
            "play_count": statistics_row["play_count"],
            "play_time": statistics_row["play_time"],
            "total_score": statistics_row["total_score"],
            "total_hits": statistics_row["total_hits"],
            "maximum_combo": statistics_row["maximum_combo"],
            "replays_watched_by_others": statistics_row["replays_watched_by_others"],
            "is_ranked": statistics_row["is_ranked"],
            # TODO
            "grade_counts": {"ss": 10, "ssh": 5, "s": 50, "sh": 0, "a": 40},
            "rank": {"global": 15000, "country": 30000},  # TODO: where is this used?
        },
        "support_level": 3,  # TODO: what's this?
        "user_achievements": [  # TODO
            # {"achieved_at": "2020-01-01T00:00:00+00:00", "achievement_id": 1}
        ],
        "rank_history": {  # TODO
            "mode": "osu",
            "data": [
                # 16200, 15500, 15000
            ],
        },
    }

    return resp

    # return {
    #     "id": 1,
    #     "join_date": "2010-01-01T00:00:00+00:00",  # "2020-01-01T00:00:00Z",
    #     "username": "cmyui",
    #     "previous_usernames": [],
    #     "country": "CN",
    #     "profile_colour": "#000000",
    #     "avatar_url": "https://avatars.githubusercontent.com/u/61514399",
    #     "cover_url": "https://assets.ppy.sh/user-profile-covers/1/0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef.jpeg",
    #     "cover": models.UserCover(
    #         custom_url="https://avatars.githubusercontent.com/u/61514399",
    #         url="https://avatars.githubusercontent.com/u/61514399",
    #         id=1,
    #     ),
    #     "is_admin": True,
    #     "is_supporter": True,
    #     "support_level": 3,
    #     "is_gmt": True,
    #     "is_qat": True,
    #     "is_bng": True,
    #     "is_bot": True,
    #     "is_active": True,
    #     "is_online": True,
    #     "pm_friends_only": True,
    #     "interests": "wtff",  # TODO
    #     "occupation": "wtff",  # TODO
    #     "title": "wtff",  # TODO
    #     "location": "CA",  # TODO
    #     "last_visit": 0,  # "2020-01-01T00:00:00Z",
    #     "twitter": "cmyui_",  # TODO
    #     "discord": "cmyui#0425",
    #     "website": "https://cmyui.com",
    #     "post_count": 0,
    #     "comments_count": 0,
    #     "follower_count": 0,
    #     "mapping_follower_count": 0,
    #     "favourite_beatmapset_count": 0,
    #     "graveyard_beatmapset_count": 0,
    #     "loved_beatmapset_count": 0,
    #     "ranked_beatmapset_count": 0,
    #     "pending_beatmapset_count": 0,
    #     "guest_beatmapset_count": 0,
    #     "scores_best_count": 0,
    #     "scores_first_count": 0,
    #     "scores_recent_count": 0,
    #     "scores_pinned_count": 0,
    #     "beatmap_playcounts_count": 0,
    #     "playstyle": ["keyboard"],  # TODO
    #     "playmode": "osu",  # TODO
    #     "profile_order": "",  # TODO
    #     "kudosu": models.KudosuCount(
    #         total=0,
    #         available=0,
    #     ),
    #     "statistics": None,  # TODO
    #     "rank_history": models.APIRankHistory(mode="osu!", data=[]),
    #     "user_achievements": [],  # list[APIUserAchievement]
    #     "monthly_playcounts": [],  # list[APIUserHistoryCount]
    #     "replays_watched_counts": [],  # list[APIUserHistoryCount]
    #     "user_achievements": [],  # list[APIUserAchievement]
    #     "statistics_rulesets": None,  # TODO https://github.com/ppy/osu/blob/master/osu.Game/Online/API/Requests/Responses/APIUser.cs#L240
    # }


@router.get("/friends", response_model=list[int])
async def get_current_friends(
    session: models.Session = Depends(usecases.sessions.authenticate),
):
    rows = await services.database.fetch_all(
        "SELECT user_b FROM user_relations "
        "WHERE user_a = :user_a AND blocked IS FALSE",
        {"user_a": session["id"]},
    )

    return [row["user_b"] for row in rows]


class UserCompact(BaseModel):
    id: int
    username: str
    profile_colour: str
    avatar_url: str
    country_code: str
    is_active: bool
    is_bot: bool
    is_deleted: bool
    is_online: bool
    is_supporter: bool


class SeasonalBackground(BaseModel):
    url: str
    user: UserCompact


class SeasonalBackgroundsResponse(BaseModel):
    ends_at: datetime
    backgrounds: list[SeasonalBackground]


class Context:
    ...


@router.get("/seasonal-backgrounds", response_model=SeasonalBackgroundsResponse)
async def get_seasonal_backgrounds(
    context: Context = Depends(),
    session: models.Session = Depends(usecases.sessions.authenticate),
):
    backgound_rows = [
        dict(row)  # take mutable copies; we'll need to add more fields
        for row in await services.database.fetch_all(
            "SELECT * FROM seasonal_backgrounds",
        )
    ]

    for background_row in backgound_rows:
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

    return {
        "ends_at": "2023-01-01T00:00:00+00:00",
        "backgrounds": backgound_rows,
    }
