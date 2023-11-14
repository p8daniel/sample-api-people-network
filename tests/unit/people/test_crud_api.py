
from app.models.common import QueryPagination
from app.models.peoples import PersonUserInfo
from app.testing.neo4j_client_mock import TestDBInterface
from tests.unit.people.data.sample_people import (
    SAMPLE_PERSON,
    SAMPLE_PERSON_JSON,
    THREE_SAMPLE_PEOPLE,
    THREE_SAMPLE_PEOPLE_JSON,
)


def test_get_all_peoples(mocker, client):
    count_mocker = mocker.patch.object(TestDBInterface, "count_people", return_value=15)
    get_mocker = mocker.patch.object(
        TestDBInterface,
        "get_people_paginated",
        return_value=THREE_SAMPLE_PEOPLE,
    )
    response = client.get("/v0/people")
    assert response.json() == {
        "data": THREE_SAMPLE_PEOPLE_JSON,
        "meta": {"pagination": {"page[number]": 0, "page[size]": 3, "page[total]": 2}},
    }
    assert count_mocker.call_count == 1
    assert list(get_mocker.call_args) == [(QueryPagination(limit=10, skip=0),), {}]


def test_get_one_person_by_id(mocker, client):
    get_mocker = mocker.patch.object(
        TestDBInterface,
        "find_person_by_id",
        return_value=SAMPLE_PERSON,
    )
    response = client.get("/v0/people/abcb029f-9562-46db-bfc9-b3fb00b60e2e")
    assert response.json() == {
        "data": SAMPLE_PERSON_JSON,
        "meta": None,
    }
    assert list(get_mocker.call_args) == [
        (),
        {"person_id": "abcb029f-9562-46db-bfc9-b3fb00b60e2e"},
    ]


def test_create_one_person(mocker, client):
    create_mocker = mocker.patch.object(
        TestDBInterface, "create_person", return_value=SAMPLE_PERSON
    )
    person_info = {
        "firstName": "the_first_name",
        "lastName": "the_last_name",
        "nickname": "the_nickname",
        "parentOf": [
            "09dda876-c0e6-4139-92f1-316db588ec5a",
            "09dda876-c0e6-4139-92f1-316db588ec5a",
        ],
        "childOf": ["889b6843-f3d1-45fc-a7a3-002772628817"],
        "friendOf": [
            "f1e00da1-6a03-4854-a966-018735cbea75",
            "0f8e072c-6b0f-42a9-93f1-efcf186e8081",
        ],
    }
    response = client.post("/v0/people", json=person_info)
    assert response.json() == {
        "data": SAMPLE_PERSON_JSON,
        "meta": None,
    }

    assert list(create_mocker.call_args) == [
        (),
        {
            "person_data": PersonUserInfo(
                first_name="the_first_name",
                last_name="the_last_name",
                nickname="the_nickname",
                parent_of=[
                    "09dda876-c0e6-4139-92f1-316db588ec5a",
                    "09dda876-c0e6-4139-92f1-316db588ec5a",
                ],
                child_of=["889b6843-f3d1-45fc-a7a3-002772628817"],
                friend_of=[
                    "f1e00da1-6a03-4854-a966-018735cbea75",
                    "0f8e072c-6b0f-42a9-93f1-efcf186e8081",
                ],
            )
        },
    ]


def test_create_one_person_minimal(mocker, client):
    create_mocker = mocker.patch.object(
        TestDBInterface, "create_person", return_value=SAMPLE_PERSON
    )
    person_info = {
        "firstName": "the_first_name",
        "lastName": "the_last_name",
    }
    response = client.post("/v0/people", json=person_info)
    assert response.json() == {
        "data": SAMPLE_PERSON_JSON,
        "meta": None,
    }

    assert list(create_mocker.call_args) == [
        (),
        {
            "person_data": PersonUserInfo(
                first_name="the_first_name",
                last_name="the_last_name",
                nickname=None,
                parent_of=[],
                child_of=[],
                friend_of=[],
            )
        },
    ]


def test_edit_one_person(mocker, client):
    edit_mocker = mocker.patch.object(TestDBInterface, "update_person", return_value=SAMPLE_PERSON)
    person_info = {
        "firstName": "the_first_name",
        "lastName": "the_last_name",
        "nickname": "the_nickname",
        "parentOf": [
            "09dda876-c0e6-4139-92f1-316db588ec5a",
            "09dda876-c0e6-4139-92f1-316db588ec5a",
        ],
        "childOf": ["889b6843-f3d1-45fc-a7a3-002772628817"],
        "friendOf": [
            "f1e00da1-6a03-4854-a966-018735cbea75",
            "0f8e072c-6b0f-42a9-93f1-efcf186e8081",
        ],
    }
    response = client.put("/v0/people/0f8e072c-6b0f-42a9-93f1-efcf186e8081", json=person_info)
    assert response.json() == {
        "data": SAMPLE_PERSON_JSON,
        "meta": None,
    }

    assert list(edit_mocker.call_args) == [
        (),
        {
            "person_data": PersonUserInfo(
                first_name="the_first_name",
                last_name="the_last_name",
                nickname="the_nickname",
                parent_of=[
                    "09dda876-c0e6-4139-92f1-316db588ec5a",
                    "09dda876-c0e6-4139-92f1-316db588ec5a",
                ],
                child_of=["889b6843-f3d1-45fc-a7a3-002772628817"],
                friend_of=[
                    "f1e00da1-6a03-4854-a966-018735cbea75",
                    "0f8e072c-6b0f-42a9-93f1-efcf186e8081",
                ],
            ),
            "person_id": "0f8e072c-6b0f-42a9-93f1-efcf186e8081",
        },
    ]


def test_delete_person(mocker, client):
    delete_mocker = mocker.patch.object(TestDBInterface, "delete_person")
    response = client.delete("/v0/people/0f8e072c-6b0f-42a9-93f1-efcf186e8081")
    assert response.status_code == 204

    assert list(delete_mocker.call_args) == [
        (),
        {"person_id": "0f8e072c-6b0f-42a9-93f1-efcf186e8081"},
    ]
