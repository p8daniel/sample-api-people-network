import logging
from pathlib import Path
from typing import List, NamedTuple

import yaml

from app.core.environment import settings
from app.dp.connection import Neo4jConnection

DATA_FILE = (Path(__file__).parent.parent.parent / "data.yml").resolve(strict=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class PersonData(NamedTuple):
    """Data fields for a person"""

    firstname: str
    lastname: str
    nickname: str
    parent_of: List[str]
    child_of: List[str]
    uuid: str
    friend_of: List[str]


def create_person(connection: Neo4jConnection, person_data: PersonData):
    """Load one person into the database"""
    logger.info("Creating person %s %s", person_data.firstname, person_data.lastname)
    with connection.driver.session() as session:
        query = (
            "MERGE (p:Person "
            "{firstname: $firstname, lastname: $lastname, nickname: $nickname, uuid: $uuid}) "
            "RETURN p"
        )
        session.run(
            query,
            firstname=person_data.firstname,
            lastname=person_data.lastname,
            nickname=person_data.nickname,
            uuid=person_data.uuid,
        )

        # Create parent-child relationships
        for child_name in person_data.parent_of:
            query = (
                "MATCH (parent:Person {uuid: $uuid}), "
                "(child:Person {firstname: $child_firstname, lastname: $child_lastname}) "
                "MERGE (parent)-[:PARENT_OF]->(child)"
                "MERGE (child)-[:CHILD_OF]->(parent)"
            )
            child_firstname, child_lastname = child_name.split(" ")
            session.run(
                query,
                uuid=person_data.uuid,
                child_firstname=child_firstname,
                child_lastname=child_lastname,
            )

        # Create child-parent relationships
        for parent_name in person_data.child_of:
            query = (
                "MATCH (child:Person {uuid: $uuid}), "
                "(parent:Person {firstname: $parent_firstname, lastname: $parent_lastname}) "
                "MERGE (child)-[:CHILD_OF]->(parent)"
                "MERGE (parent)-[:PARENT_OF]->(child)"
            )
            parent_firstname, parent_lastname = parent_name.split(" ")
            session.run(
                query,
                uuid=person_data.uuid,
                parent_firstname=parent_firstname,
                parent_lastname=parent_lastname,
            )

        # Create friend links
        for friend in person_data.friend_of:
            query = (
                "MATCH (person:Person {uuid: $uuid}), "
                "(friend:Person {firstname: $friend_firstname, lastname: $friend_lastname}) "
                "MERGE (person)-[:FRIEND_OF]->(friend) "
                "MERGE (friend)-[:FRIEND_OF]->(person)"
            )
            friend_firstname, friend_lastname = friend.split(" ")
            session.run(
                query,
                uuid=person_data.uuid,
                friend_firstname=friend_firstname,
                friend_lastname=friend_lastname,
            )


def load_yaml_data_to_neo4j(yaml_file, uri, username, password):
    """load data from a YAML file and create nodes and relationships in Neo4j"""

    with yaml_file.open() as file:
        data = yaml.safe_load(file)

    with Neo4jConnection(uri=uri, username=username, password=password) as neo4j_connection:
        for person_data in data.get("people", []):
            person_data = PersonData(
                firstname=person_data.get("firstname"),
                lastname=person_data.get("lastname"),
                nickname=person_data.get("nickname"),
                parent_of=person_data.get("parent_of", []),
                child_of=person_data.get("child_of", []),
                uuid=person_data.get("uuid"),
                friend_of=person_data.get("friend_of", []),
            )
            create_person(connection=neo4j_connection, person_data=person_data)


if __name__ == "__main__":
    load_yaml_data_to_neo4j(
        yaml_file=DATA_FILE,
        uri=settings.NEO4J_URI,
        username=settings.NEO4J_USERNAME,
        password=settings.NEO4J_PASSWORD,
    )
