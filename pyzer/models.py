from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import Any
from typing import Literal
from typing import Optional
from typing import Sequence

from pydantic import BaseModel

# TODO: should pyzer & lazer models be split into separate files?

## pyzer models

# enumerations

# data models


class Session(BaseModel):
    token_type: Literal["Bearer"]
    access_token_expiry: int
    access_token: str
    refresh_token: str

    id: int
    username: str


## osu!api v2 (taken from lazer code) models

# enumerations


class Privileges:
    ...


# data models


class UserCover(BaseModel):
    # NOTE: this doesn't have type definition on osu wiki
    custom_url: str  # "https://c.ppy.sh/1"
    url: str  # "https://d.ppy.sh/1"
    id: Optional[int]


class KudosuCount(BaseModel):
    total: int
    available: int


class APIRankHistory(BaseModel):
    mode: str
    data: list[int]


class UserBadge(BaseModel):
    awarded_at: datetime
    description: str
    image_url: str
    url: str


class APIUserAchievement(BaseModel):
    achievement_id: int
    achieved_at: datetime


class APIUserHistoryCount(BaseModel):
    start_date: datetime
    count: int  # long


class Country(BaseModel):
    name: str
    code: str


class UserLevel(BaseModel):
    current: int
    progress: int


class UserRank(BaseModel):
    global_: int
    country: int


class GradeCounts(BaseModel):
    ssh: int
    ss: int
    sh: int
    s: int
    a: int


class UserStatistics(BaseModel):
    # TODO: level calculation based on total score
    level: UserLevel  # * progress 0-100
    # TODO: if score.pp is also an int in the api, then we can just make it int everywhere
    # * It's not ~Lemres
    pp: int  # ? floor this?
    global_rank: Optional[int]
    ranked_score: int
    hit_accuracy: float
    play_count: int
    play_time: int
    total_score: int
    total_hits: int
    maximum_combo: int
    replays_watched_by_others: int
    is_ranked: bool
    grade_counts: GradeCounts
    rank: UserRank  # TODO: where is this used? || User profile? ~Lemres


class DailyCountLineItem(BaseModel):
    start_date: date  # 2020-10-12
    count: int  # 50


class UserpageContent(BaseModel):
    html: str  #  "<div class='bbcode bbcode--profile-page'><center>Hello</center></div>",
    raw: str  #  "[centre]Hello[/centre]",


class UserGroup(BaseModel):
    id: int
    identifier: str  # Unique string to identify the group.
    name: str
    short_name: str  # Short name of the group for display.
    description: Optional[str]
    colour: str
    has_listing: bool  # this group displays a listing at /groups/{id}.
    has_playmodes: bool  # Whether this group associates GameModes with users' memberships.
    is_probationary: bool  # Whether members of this group are considered probationary.


class AchievementAchieval(BaseModel):
    achievement_id: int
    achieved_at: datetime


class RankHistory(BaseModel):
    mode: Literal["osu", "taiko", "catch", "mania"]
    data: list[int]


class ProfileBanner(BaseModel):
    id: int
    tournament_id: int
    image: str


class User(BaseModel):
    id: int
    # TODO: customizable subdomains?
    avatar_url: str
    country_code: str
    default_group: Literal["default"]  # TODO: what's this? # TODO: others?
    is_online: bool  # TODO: is this always true when calling this endpoint?
    is_active: bool  # ?: whats this?
    is_bot: bool
    is_supporter: bool
    is_restricted: bool  # TODO
    is_deleted: bool  # TODO: account deletions/deactivations?
    last_visit: datetime
    pm_friends_only: bool
    profile_colour: str
    username: str
    cover_url: str
    discord: str
    has_supported: bool
    interests: Optional[str]
    join_date: datetime
    kudosu: KudosuCount
    location: Optional[str]
    max_blocks: int
    max_friends: int
    occupation: Optional[str]
    playmode: Literal["osu"]  # TODO preference?
    playstyle: list[Literal["mouse", "tablet", "keyboard", "touch"]]
    post_count: int  # TODO?
    profile_order: Sequence[
        Literal[  # TODO (pg json field?)
            "me",
            "kudosu",
            "historical",
            "beatmaps",
            "recent_activity",
            "top_ranks",
            "medals",
        ]
    ]
    title: str
    twitter: str
    website: str
    country: Country
    cover: UserCover
    account_history: list[Any]  # TODO: confine this
    active_tournament_banner: Optional[ProfileBanner]
    badges: list[UserBadge]
    follower_count: int
    favourite_beatmapset_count: int  # TODO
    graveyard_beatmapset_count: int
    pending_beatmapset_count: int  # TODO
    loved_beatmapset_count: int  # TODO
    ranked_beatmapset_count: int  # TODO
    groups: list[UserGroup]  # TODO
    monthly_playcounts: list[DailyCountLineItem]
    page: UserpageContent
    previous_usernames: list[str]  # TODO || ?: store them in seperate table?
    replays_watched_counts: list[DailyCountLineItem]
    scores_first_count: int  # ? what is this? + TODO
    statistics: UserStatistics
    support_level: int  # hearts on the user's profile
    user_achievements: list[AchievementAchieval]
    rank_history: RankHistory


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
