from typing import List

from pydantic import BaseModel, Field

from app.api.api_v0.models.common import CamelModel, PayloadModel


class NameId(BaseModel):
    """Models of an id and a name"""

    person_id: str = Field(alias="ID")
    name: str


class Person(CamelModel):
    """Model for a person in the payload"""

    person_id: str = Field(alias="ID")
    first_name: str
    last_name: str
    nickname: str | None
    parent_of: List[NameId]
    child_of: List[NameId]
    friend_of: List[NameId]


class PersonCreate(CamelModel):
    """Models for info to create a Person"""

    first_name: str
    last_name: str
    nickname: str | None = None
    parent_of: List[str] = []
    child_of: List[str] = []
    friend_of: List[str] = []


class PersonUpdate(CamelModel):
    """Model info to edit a Person"""

    first_name: str
    last_name: str
    nickname: str | None = None
    parent_of: List[str] = []
    child_of: List[str] = []
    friend_of: List[str] = []


class PeoplePayload(PayloadModel):
    """Payload model to get people"""

    data: List[Person]


class PeopleIDPayload(PayloadModel):
    """Payload model to get people"""

    data: List[NameId]


class PersonPayload(PayloadModel):
    """Payload model to get one person"""

    data: Person
