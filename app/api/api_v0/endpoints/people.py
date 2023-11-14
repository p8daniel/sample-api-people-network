import dataclasses
import math
from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.api_v0.models.common import PaginationParams, get_pagination_params
from app.api.api_v0.models.person import PeoplePayload, PersonCreate, PersonPayload, PersonUpdate
from app.api.api_v0.util_functions import pagination_to_offset_limit
from app.api.dependencies import get_db_interface
from app.dao.people.interface import PeopleRepositoryInterface
from app.models.common import QueryPagination
from app.models.peoples import PersonUserInfo

router = APIRouter()


@router.get("", response_model=PeoplePayload)
async def read_people(
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
    db_interface: PeopleRepositoryInterface = Depends(get_db_interface),
) -> PeoplePayload:
    """Retrieve People"""
    offset_limit = pagination_to_offset_limit(pagination=pagination)
    people = await db_interface.get_people_paginated(
        QueryPagination(limit=offset_limit.limit, skip=offset_limit.offset)
    )
    meta = await build_meta_with_pagination(
        db_interface=db_interface, pagination=pagination, result=people
    )
    return PeoplePayload(data=[dataclasses.asdict(person) for person in people], meta=meta)


@router.get("/{id}", response_model=PersonPayload)
async def read_one_person(
    db_interface: PeopleRepositoryInterface = Depends(get_db_interface),
    person_id: str = Path(alias="id"),
) -> PersonPayload:
    """Retrieve one person by id"""
    person = await db_interface.find_person_by_id(person_id=person_id)
    return PersonPayload(data=dataclasses.asdict(person))


@router.post("", response_model=PersonPayload, status_code=201)
async def create_one_person(
    person_data: PersonCreate,
    db_interface: PeopleRepositoryInterface = Depends(get_db_interface),
) -> PersonPayload:
    """Retrieve one person by id"""
    person = await db_interface.create_person(
        person_data=PersonUserInfo(**person_data.model_dump())
    )
    return PersonPayload(data=dataclasses.asdict(person))


@router.put("/{id}", response_model=PersonPayload)
async def edit_one_person(
    person_data: PersonUpdate,
    db_interface: PeopleRepositoryInterface = Depends(get_db_interface),
    person_id: str = Path(alias="id"),
) -> PersonPayload:
    """Edit one person"""
    person = await db_interface.update_person(
        person_id=person_id, person_data=PersonUserInfo(**person_data.model_dump())
    )
    return PersonPayload(data=dataclasses.asdict(person))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_person(
    db_interface: PeopleRepositoryInterface = Depends(get_db_interface),
    person_id: str = Path(alias="id"),
) -> None:
    """Retrieve one person by id"""
    await db_interface.delete_person(person_id=person_id)


async def build_meta_with_pagination(
    result: List[Any],
    db_interface: PeopleRepositoryInterface,
    pagination: PaginationParams,
):
    """Build meta dictionary with pagination for the payload"""
    count_results = len(result)
    meta = {}
    total_count = await db_interface.count_people()
    meta["pagination"] = {
        "page[size]": count_results,
        "page[number]": pagination.page_number,
        "page[total]": math.ceil(total_count / pagination.page_size),
    }
    return meta
