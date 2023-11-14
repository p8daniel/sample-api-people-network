from dataclasses import dataclass
from typing import List


@dataclass
class NameIdDataclass:
    """Business model for a person id and a name"""

    ID: str
    name: str


@dataclass
class PersonDataclass:
    """Business model for a person"""

    ID: str
    first_name: str
    last_name: str
    nickname: str | None
    parent_of: List[NameIdDataclass]
    child_of: List[NameIdDataclass]
    friend_of: List[NameIdDataclass]


@dataclass
class PersonUserInfo:
    """Business model for a person info for edition or creation"""

    first_name: str
    last_name: str
    nickname: str | None
    parent_of: List[str]
    child_of: List[str]
    friend_of: List[str]
