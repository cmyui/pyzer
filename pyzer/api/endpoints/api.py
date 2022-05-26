import json
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from pyzer import models
from pyzer import services
from pyzer import settings

router = APIRouter(prefix="/api")

# oauth2: https://tools.ietf.org/id/draft-richer-oauth-json-request-00.html
security = HTTPBearer()


async def authorize_session(
    token: HTTPAuthorizationCredentials = Depends(security),
) -> Optional[models.Session]:
    session = await services.redis_sessions_db.get(token.credentials)
    if session is None:
        return None

    return models.Session(**json.loads(session))


# TODO: figure out what to do about this
def country_code_to_long_form(country_code: str) -> str:
    return {
        "AU": "Australia",
        "CA": "Canada",
    }[country_code]


# NOTE - the trailing `/` matters?
# TODO: is this to differentiate lazer?
@router.get("/v2/me/")
async def get_current_user(session: models.Session = Depends(authorize_session)):
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

    user_id = user_row["id"]

    resp = {
        "id": user_id,
        # TODO: customizable subdomains?
        "avatar_url": f"https://a.{settings.DOMAIN}/{user_id}.jpeg",
        "country_code": user_row["country"],
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
            "code": user_row["country"],
            "name": country_code_to_long_form(user_row["country"]),
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


@router.get("/v2/friends")
async def get_current_friends(session: models.Session = Depends(authorize_session)):
    friend_ids: list[int] = []
    return friend_ids


# TODO: not even sure when this is used
# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     while True:
#         data = await websocket.receive()
#         await websocket.send(data)
