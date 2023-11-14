import pytest
from starlette.testclient import TestClient

from app.api.dependencies import get_db_interface
from app.main import app
from app.testing.neo4j_client_mock import TestDBInterface




@pytest.fixture()
def client():
    def override_get_db():
        return TestDBInterface()

    app.dependency_overrides[get_db_interface] = override_get_db
    client = TestClient(app)

    yield client
