from app.models.peoples import NameIdDataclass
from app.testing.neo4j_client_mock import TestDBInterface
from tests.unit.people.data.sample_people import SAMPLE_ANCESTORS


def test_get_person_ancestors(mocker, client):
    get_mocker = mocker.patch.object(
        TestDBInterface,
        "get_ancestors_by_person_id",
        return_value=SAMPLE_ANCESTORS,
    )
    response = client.get("/v0/people/abcb029f-9562-46db-bfc9-b3fb00b60e2e/ancestors")
    assert response.json() == {
        "data": [
            {"ID": "10d11ded-8550-44ac-9a30-1c5b453fe801", "name": "Zoe Taylor"},
            {"ID": "a2e47d96-2a7c-4132-a9e6-fbc5ddd2c05f", "name": "Richard Taylor"},
            {"ID": "034d840e-7d35-4c0e-9bc5-a82b9d2f7fa7", "name": "Grace Taylor"},
        ],
        "meta": None,
    }
    assert list(get_mocker.call_args) == [
        (),
        {"person_id": "abcb029f-9562-46db-bfc9-b3fb00b60e2e"},
    ]


def test_get_family_friends(mocker, client):
    get_mocker = mocker.patch.object(
        TestDBInterface,
        "get_family_fiends",
        return_value=[
            NameIdDataclass(ID="01ddd2b4-2369-44bc-9429-7de51c3d3c61", name="George Brown")
        ],
    )
    response = client.get("/v0/people/abcb029f-9562-46db-bfc9-b3fb00b60e2e/familyFriends")
    assert response.json() == {
        "data": [{"ID": "01ddd2b4-2369-44bc-9429-7de51c3d3c61", "name": "George Brown"}],
        "meta": None,
    }
    assert list(get_mocker.call_args) == [
        (),
        {"person_id": "abcb029f-9562-46db-bfc9-b3fb00b60e2e"},
    ]
