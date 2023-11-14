from typing import Dict, List
from uuid import uuid4

from neo4j import ManagedTransaction

from app.models.common import QueryPagination
from app.models.peoples import PersonUserInfo


def get_people_nodes_with_pagination(
    transaction: ManagedTransaction, pagination: QueryPagination, person_id: str | None = None
) -> List[Dict]:
    """Return the people with limit and offset on the result"""
    params = pagination._asdict()
    if person_id is not None:
        params["uuid"] = person_id
    filter_uuid_string = "{uuid: $uuid}"
    query = (
        "MATCH (person:Person "
        f"{filter_uuid_string if person_id is not None else ''}"
        ") "
        """
        WITH person
        ORDER BY person.firstname, person.lastname DESC SKIP $skip LIMIT $limit
        OPTIONAL MATCH (person:Person)-[:PARENT_OF]->(child)
        OPTIONAL MATCH (person:Person)-[:CHILD_OF]->(parent)
        OPTIONAL MATCH (person:Person)-[:FRIEND_OF]->(friend)
        RETURN person, child, parent, friend
        """
    )
    result = transaction.run(
        query,
        **params,
    )
    return [record.data() for record in list(result)]


def count_people_nodes(transaction: ManagedTransaction) -> List[Dict]:
    """Return the total number of people"""
    result = transaction.run(
        """
        MATCH (p:Person)
        RETURN count(p)
        """
    )
    return [record.data() for record in list(result)]


def create_new_person_node(
    transaction: ManagedTransaction, person_data: PersonUserInfo, uuid: str | None | None
) -> List[Dict]:
    """Return the total number of people"""
    query_variables = ["firstname: $firstname", "lastname: $lastname", "uuid: $uuid"]
    params = {
        "firstname": person_data.first_name,
        "lastname": person_data.last_name,
        "uuid": uuid if uuid is not None else str(uuid4()),
    }
    if person_data.nickname is not None:
        params["nickname"] = person_data.nickname
        query_variables.append("nickname: $nickname")
    query = f"MERGE (p:Person {{{', '.join(query_variables)}}}) " "RETURN p"
    result = transaction.run(
        query,
        **params,
    )
    return [record.data() for record in list(result)]


def link_child_to_parent(transaction: ManagedTransaction, parent_id: str, child_id: str) -> None:
    """Execute Query to link child and parent"""
    query = (
        "MATCH (parent:Person {uuid: $parent_id}), "
        "(child:Person {uuid: $child_id}) "
        "MERGE (parent)-[:PARENT_OF]->(child) "
        "MERGE (child)-[:CHILD_OF]->(parent)"
    )
    transaction.run(
        query,
        parent_id=parent_id,
        child_id=child_id,
    )


def link_friends(transaction: ManagedTransaction, person1_id: str, person2_id: str) -> None:
    """Execute Query to link child and parent"""
    query = (
        "MATCH (person1:Person {uuid: $person1_id}), "
        "(person2:Person {uuid: $person2_id}) "
        "MERGE (person1)-[:FRIEND_OF]->(person2) "
        "MERGE (person2)-[:FRIEND_OF]->(person1)"
    )
    transaction.run(
        query,
        person1_id=person1_id,
        person2_id=person2_id,
    )


def delete_one_person_query(transaction: ManagedTransaction, person_id: str) -> None:
    """Query to delete a person"""
    query = "MATCH (person:Person {uuid: $person_id}) DETACH DELETE person "
    transaction.run(
        query,
        person_id=person_id,
    )


def get_ancestors_query(transaction: ManagedTransaction, person_id: str) -> List[Dict]:
    """Query to get ancestors"""
    query = (
        "MATCH (person:Person{uuid: $person_id})-[:CHILD_OF *1..]->(ancestor:Person)  "
        "RETURN ancestor"
    )
    result = transaction.run(
        query,
        person_id=person_id,
    )
    return [record.data() for record in list(result)]


def get_family_friend(transaction: ManagedTransaction, person_id: str) -> List[Dict]:
    """Query to get family friends"""
    query = """
        MATCH (p:Person{uuid: $uuid})
        WITH p
        CALL apoc.path.expandConfig(p, {
                relationshipFilter: '<CHILD_OF|<PARENT_OF',
                uniqueness: 'NODE_GLOBAL'
            }) yield path
        WITH last(nodes(path)) as related
        MATCH(related:Person)-[:FRIEND_OF]->(friend:Person)
        RETURN friend
    """
    result = transaction.run(
        query,
        uuid=person_id,
    )
    return [record.data() for record in list(result)]
