from datetime import datetime
from typing import Optional

from pyzer import models
from pyzer import services
from pyzer import settings

# TODO: figure out what to do about this
def country_code_to_name(country_code: str) -> str:
    return {
        "AU": "Australia",
        "CA": "Canada",
    }[country_code]


async def fetch_friends_by_id(id: int) -> list[int]:
    rows = await services.database.fetch_all(
        "SELECT user_b FROM user_relations "
        "WHERE user_a = :user_a AND blocked IS FALSE",
        {"user_a": id},
    )

    return [row["user_b"] for row in rows]


async def fetch_by_id(id: int) -> Optional[models.User]:
    # validate credentials
    user_row = await services.database.fetch_one(
        "SELECT * FROM users WHERE id = :id",
        {"id": id},
    )
    if user_row is None:
        print(1111, flush=True)
        return None  # TODO: what's correct error?

    statistics_row = await services.database.fetch_one(
        "SELECT * FROM user_statistics WHERE id = :id",
        {"id": id},
    )
    if statistics_row is None:
        print(1111, flush=True)
        return None  # TODO: what's correct error?

    return models.User(
        id=user_row["id"],
        avatar_url=f"https://a.{settings.DOMAIN}/{user_row['id']}.jpeg",
        country_code=user_row["country_code"],
        default_group="default",
        is_active=True,
        is_bot=user_row["is_bot"],
        is_deleted=False,  # TODO: account deletions/deactivations?
        is_online=True,  # TODO: is this always true when calling this endpoint?
        is_supporter=user_row["is_supporter"],
        last_visit="2020-01-01T00:00:00+00:00",  # TODO
        pm_friends_only=user_row["pm_friends_only"],
        profile_colour=user_row["profile_colour"],
        username=user_row["username"],
        cover_url="https://assets.ppy.sh/user-profile-covers/1/0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef.jpeg",  # TODO
        discord=user_row["discord"],
        has_supported=user_row["has_supported"],
        interests=user_row["interests"],  # NOTE: nullable
        join_date=user_row["join_date"].isoformat(),  # "2010-01-01T00:00:00+00:00",
        kudosu=models.KudosuCount(
            total=user_row["kudosu_total"],
            available=user_row["kudosu_available"],
        ),
        location=user_row["location"],  # NOTE: nullable
        max_blocks=user_row["max_blocks"],
        max_friends=user_row["max_friends"],
        occupation=user_row["occupation"],  # NOTE: nullable
        playmode="osu",  # TODO preference?
        playstyle=["mouse", "tablet", "keyboard", "touch"],  # TODO
        post_count=0,  # TODO?
        profile_order=[  # TODO (pg json field?)
            "me",
            "recent_activity",
            "beatmaps",
            "historical",
            "kudosu",
            "top_ranks",
            "medals",
        ],
        title=user_row["title"],  # TODO
        twitter=user_row["twitter"],
        website=user_row["website"],
        country=models.Country(  # TODO, and also why is code duplicated
            code=user_row["country_code"],
            name=country_code_to_name(user_row["country_code"]),
        ),
        cover=models.UserCover(  # TODO, and also why is code duplicated
            custom_url="https://x.catboy.best/21PPQcH.png",
            url="https://x.catboy.best/21PPQcH.png",
            id=None,
        ),
        is_restricted=False,  # TODO
        account_history=[],  # TODO: whats this?
        active_tournament_banner=models.ProfileBanner(
            id=0,
            tournament_id=0,
            image="real",
        ),
        badges=[  # TODO
            models.UserBadge(
                awarded_at="2015-01-01T00:00:00+00:00",
                description="Test badge",
                image_url="https://assets.ppy.sh/profile-badges/test.png",
                url="",
            ),
        ],
        favourite_beatmapset_count=0,  # TODO
        follower_count=user_row["follower_count"],
        graveyard_beatmapset_count=0,  # TODO
        groups=[  # TODO
            # {
            #     "id": 1,
            #     "identifier": "gmt",
            #     "name": "gmt",
            #     "short_name": "GMT",
            #     "description": "",
            #     "colour": "#FF0000",
            # }
        ],
        loved_beatmapset_count=0,  # TODO
        monthly_playcounts=[  # TODO
            models.DailyCountLineItem(start_date="2019-11-01", count=100),
            models.DailyCountLineItem(start_date="2019-12-01", count=150),
            models.DailyCountLineItem(start_date="2020-01-01", count=20),
        ],
        page=models.UserpageContent(  # TODO
            html="<div class='bbcode bbcode--profile-page'><center>Hello</center></div>",
            raw="[centre]Hello[/centre]",
        ),
        pending_beatmapset_count=0,  # TODO
        previous_usernames=[],  # TODO
        ranked_beatmapset_count=0,  # TODO
        replays_watched_counts=[  # TODO
            models.DailyCountLineItem(start_date="2019-11-01", count=100),
            models.DailyCountLineItem(start_date="2019-12-01", count=150),
            models.DailyCountLineItem(start_date="2020-01-01", count=20),
        ],
        scores_first_count=0,  # TDOO
        statistics=models.UserStatistics(
            # TODO: level calculation based on total score
            level=models.UserLevel(current=0, progress=0),  # progress 0-100
            # TODO: if score.pp is also an int in the api,
            # then we can just make it int everywhere
            pp=int(statistics_row["pp"]),
            global_rank=statistics_row["global_rank"],
            ranked_score=statistics_row["ranked_score"],
            hit_accuracy=statistics_row["hit_accuracy"],
            play_count=statistics_row["play_count"],
            play_time=statistics_row["play_time"],
            total_score=statistics_row["total_score"],
            total_hits=statistics_row["total_hits"],
            maximum_combo=statistics_row["maximum_combo"],
            replays_watched_by_others=statistics_row["replays_watched_by_others"],
            is_ranked=statistics_row["is_ranked"],
            # TODO
            grade_counts={"ss": 10, "ssh": 5, "s": 50, "sh": 0, "a": 40},
            rank=models.UserRank(
                global_=15000,
                country=30000,
            ),  # TODO: where is this used?
        ),
        support_level=3,  # TODO: what's this?
        user_achievements=[  # TODO
            models.AchievementAchieval(
                achieved_at=datetime.fromisoformat("2020-01-01T00:00:00+00:00"),
                achievement_id=1,
            ),
        ],
        rank_history=models.RankHistory(  # TODO
            mode="osu",
            data=[16200, 15500, 15000],
        ),
    )
