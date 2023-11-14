import dataclasses

from fastapi import APIRouter, Depends, Path

from app.api.api_v0.models.person import PeopleIDPayload
from app.api.dependencies import get_db_interface
from app.dao.people.interface import PeopleRepositoryInterface

router = APIRouter()


@router.get("/{id}/ancestors", response_model=PeopleIDPayload)
async def get_person_ancestors(
    db_interface: PeopleRepositoryInterface = Depends(get_db_interface),
    person_id: str = Path(alias="id"),
) -> PeopleIDPayload:
    """Retrieve one person ancestors by id"""
    people = await db_interface.get_ancestors_by_person_id(person_id=person_id)
    return PeopleIDPayload(data=[dataclasses.asdict(person) for person in people])


@router.get("/{id}/familyFriends", response_model=PeopleIDPayload)
async def get_person_family_friends(
    db_interface: PeopleRepositoryInterface = Depends(get_db_interface),
    person_id: str = Path(alias="id"),
) -> PeopleIDPayload:
    """Retrieve one person ancestors by id"""
    people = await db_interface.get_family_fiends(person_id=person_id)
    return PeopleIDPayload(data=[dataclasses.asdict(person) for person in people])
