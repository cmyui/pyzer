from datetime import datetime
from typing import Literal
from typing import TypedDict

# TODO: should pyzer & lazer models be split into separate files?


## pyzer models

# enumerations

# data models


class Session(TypedDict):
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


class UserCover(TypedDict):
    custom_url: str  # "https://c.ppy.sh/1"
    url: str  # "https://d.ppy.sh/1"
    id: str  # 1


class KudosuCount(TypedDict):
    total: int
    available: int


class APIRankHistory(TypedDict):
    mode: str
    data: list[int]


class Badge(TypedDict):
    awarded_at: datetime
    description: str
    image_url: str


class APIUserAchievement(TypedDict):
    achievement_id: int
    achieved_at: datetime


class APIUserHistoryCount(TypedDict):
    start_date: datetime
    count: int  # long
