import os
from pathlib import Path

import httpx
import pytest

from app.dao.people.interface import PeopleNeo4JDAO
from app.dp.connection import Neo4jConnection
from app.dp.init_db import load_yaml_data_to_neo4j

NEO4J_URI = os.environ.get("NEO4J_URI", "neo4j://localhost:7687")
SERVICE_URL = os.environ.get("SERVICE_URL", "http://localhost:5000")
DATA_FILE = (Path(__file__).parent.parent.parent / "data.yml").resolve(strict=True)

@pytest.fixture()
def db_session():
    connection = Neo4jConnection(NEO4J_URI)
    with connection.driver.session() as session:
        yield PeopleNeo4JDAO(db_session=session)


@pytest.fixture()
def test_client():
    client = httpx.Client(base_url=SERVICE_URL, timeout=1000)
    yield client


@pytest.fixture(autouse=True, scope="session")
def load_data_into_db():
    load_yaml_data_to_neo4j(
        yaml_file=DATA_FILE,
        uri=NEO4J_URI,
        username="",
        password=""
    )
