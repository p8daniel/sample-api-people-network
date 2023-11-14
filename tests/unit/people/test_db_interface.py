import dataclasses
import json
from pathlib import Path

from app.dao.people.interface import PeopleNeo4JDAO
from app.models.common import QueryPagination
from app.models.peoples import NameIdDataclass, PersonDataclass
from app.testing.neo4j_client_mock import TestGraphDatabaseSession
from app.testing.utils_functions import order_json
from tests.unit.people.data.sample_people import LIST_PEOPLE

DATA_FOLDER = (Path(__file__).parent / "data").resolve(strict=True)


async def test_get_people(mocker):
    db_interface = PeopleNeo4JDAO(db_session=TestGraphDatabaseSession)
    with (DATA_FOLDER / "result_query_get_all.json").open() as json_file:
        query_result = json.load(json_file)
    read_mocker = mocker.patch.object(
        TestGraphDatabaseSession, "execute_read", return_value=query_result
    )
    result = await db_interface.get_people_paginated(QueryPagination(skip=12, limit=100))

    assert order_json([dataclasses.asdict(person) for person in result]) == order_json(
        [dataclasses.asdict(person) for person in LIST_PEOPLE]
    )
    assert read_mocker.call_args.kwargs == {"pagination": QueryPagination(limit=100, skip=12)}


async def test_get_one_person(mocker):
    db_interface = PeopleNeo4JDAO(db_session=TestGraphDatabaseSession)
    with (DATA_FOLDER / "one_person_query_result.json").open() as json_file:
        query_result = json.load(json_file)
    read_mocker = mocker.patch.object(
        TestGraphDatabaseSession, "execute_read", return_value=query_result
    )
    result = await db_interface.find_person_by_id(person_id="abcb029f-9562-46db-bfc9-b3fb00b60e2e")

    assert order_json(dataclasses.asdict(result)) == order_json(
        dataclasses.asdict(
            PersonDataclass(
                ID="abcb029f-9562-46db-bfc9-b3fb00b60e2e",
                first_name="Anna",
                last_name="Smith",
                nickname="Annie",
                parent_of=[
                    NameIdDataclass(ID="801225df-d5e1-4b01-adae-0cca392608da", name="Susan Smith"),
                    NameIdDataclass(ID="4b3df73f-0174-4c20-b82c-89a1466689cb", name="John Smith"),
                ],
                child_of=[
                    NameIdDataclass(ID="94c245b1-3be2-4eda-8737-e559f8cac2e5", name="Lisa Smith")
                ],
                friend_of=[],
            )
        )
    )
    assert read_mocker.call_args.kwargs == {
        "pagination": QueryPagination(limit=1, skip=0),
        "person_id": "abcb029f-9562-46db-bfc9-b3fb00b60e2e",
    }
