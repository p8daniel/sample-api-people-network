from typing import Dict, NamedTuple

import pytest

from app.testing.people import get_people_with_pagination
from app.testing.utils_functions import UUID_REGEX, MatchRegex


class Payloads(NamedTuple):
    to_send: Dict
    reference: Dict


@pytest.fixture
def initial_person():
    post_payload = {
        "firstName": "Olivia",
        "lastName": "Anderson",
        "nickname": "Sparky",
        "parentOf": ["13478bb6-367d-4c2a-ada4-80877b1ef8a4"],
        "childOf": ["94c245b1-3be2-4eda-8737-e559f8cac2e5"],
        "friendOf": ["e708394e-935c-405d-b2a2-6d68a1470d41"],
    }
    get_payload = {
        "ID": MatchRegex(UUID_REGEX),
        "firstName": "Olivia",
        "lastName": "Anderson",
        "nickname": "Sparky",
        "parentOf": [{"ID": "13478bb6-367d-4c2a-ada4-80877b1ef8a4", "name": "Victor Smith"}],
        "childOf": [{"ID": "94c245b1-3be2-4eda-8737-e559f8cac2e5", "name": "Lisa Smith"}],
        "friendOf": [{"ID": "e708394e-935c-405d-b2a2-6d68a1470d41", "name": "James Brown"}],
    }
    return Payloads(to_send=post_payload, reference=get_payload)


@pytest.fixture
def updated_person() -> Payloads:
    put_payload = {
        "firstName": "Liam",
        "lastName": "Williams",
        "nickname": "Luna",
        "parentOf": [
            "223bae59-f829-401b-a985-08b37d6eb1c7",
        ],
        "childOf": ["08adfb73-5242-42e1-a360-3117097d8fea"],
        "friendOf": [
            "141574ad-be93-449d-9730-469d997d8562",
        ],
    }
    get_payload = {
        "ID": MatchRegex(UUID_REGEX),
        "firstName": "Liam",
        "lastName": "Williams",
        "nickname": "Luna",
        "parentOf": [{"ID": "223bae59-f829-401b-a985-08b37d6eb1c7", "name": "Ella Brown"}],
        "childOf": [{"ID": "08adfb73-5242-42e1-a360-3117097d8fea", "name": "Ruby Brown"}],
        "friendOf": [{"ID": "141574ad-be93-449d-9730-469d997d8562", "name": "Emily Stevens"}],
    }
    return Payloads(to_send=put_payload, reference=get_payload)


def test_people_crud_scenario(test_client, initial_person, updated_person):
    created_person = (test_client.post("/v0/people", json=initial_person.to_send)).json()["data"]
    person_id = created_person["ID"]
    get_initial_person = (test_client.get(f"/v0/people/{person_id}")).json()["data"]
    assert created_person == get_initial_person
    assert get_initial_person == initial_person.reference
    all_people = get_people_with_pagination(client=test_client)
    assert person_id in [person["ID"] for person in all_people]
    edited_person = (
        test_client.put(f"/v0/people/{person_id}", json=updated_person.to_send)
    ).json()["data"]
    get_edited_person = (test_client.get(f"/v0/people/{person_id}")).json()["data"]
    assert edited_person == get_edited_person
    assert get_edited_person == updated_person.reference

    delete_response = test_client.delete(f"/v0/people/{person_id}")
    assert delete_response.status_code == 204
    get_after_delete = test_client.get(f"/v0/people/{person_id}")
    assert get_after_delete.status_code == 404


def test_get_ancestors(test_client):
    response = test_client.get("/v0/people/411ad976-e0e2-4cfa-a5ef-916552d45b9d/ancestors")
    data = response.json()["data"]
    assert data == [
        {"ID": "10d11ded-8550-44ac-9a30-1c5b453fe801", "name": "Zoe Taylor"},
        {"ID": "a2e47d96-2a7c-4132-a9e6-fbc5ddd2c05f", "name": "Richard Taylor"},
        {"ID": "034d840e-7d35-4c0e-9bc5-a82b9d2f7fa7", "name": "Grace Taylor"},
    ]


def test_get_family_friends(test_client):
    response = test_client.get("/v0/people/3d660778-d473-4042-8670-95d7451fa32c/familyFriends")
    data = response.json()["data"]
    assert data == [{"ID": "01ddd2b4-2369-44bc-9429-7de51c3d3c61", "name": "George Brown"}]
