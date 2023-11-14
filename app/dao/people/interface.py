from typing import List, Protocol

from neo4j import Session

from app.dao.people.constructors import construct_people_list_from_query_result
from app.dao.people.cypher_queries import (
    count_people_nodes,
    create_new_person_node,
    delete_one_person_query,
    get_ancestors_query,
    get_family_friend,
    get_people_nodes_with_pagination,
    link_child_to_parent,
    link_friends,
)
from app.errors.app_errors import Neo4JError, NotFoundError
from app.models.common import QueryPagination
from app.models.peoples import NameIdDataclass, PersonDataclass, PersonUserInfo


class PeopleRepositoryInterface(Protocol):
    """Repository interface for peoples"""

    async def get_people_paginated(self, pagination: QueryPagination) -> List[PersonDataclass]:
        """Get all people"""
        ...

    async def count_people(self) -> int:
        """Get the number of people"""
        ...

    async def find_person_by_id(self, person_id: str) -> PersonDataclass:
        """Find a person by its ID"""
        ...

    async def create_person(
        self, person_data: PersonUserInfo, uuid: str | None = None
    ) -> PersonDataclass:
        """Create a new person"""
        ...

    async def update_person(self, person_data: PersonUserInfo, person_id: str) -> PersonDataclass:
        """Edit a person"""
        ...

    async def delete_person(self, person_id: str) -> None:
        """Delete a person from id"""
        ...

    async def get_ancestors_by_person_id(self, person_id: str) -> List[NameIdDataclass]:
        """Get the person ancestors"""
        ...

    async def get_family_fiends(self, person_id: str) -> List[NameIdDataclass]:
        """Get the person family friend"""
        ...


class PeopleNeo4JDAO:
    """Noe4j interface for peoples"""

    def __init__(self, db_session: Session) -> None:
        self.session = db_session

    async def get_people_paginated(self, pagination: QueryPagination) -> List[PersonDataclass]:
        """Get all people"""
        query_result = await self.execute_read(
            get_people_nodes_with_pagination, pagination=pagination
        )

        people = construct_people_list_from_query_result(query_result)
        return people

    async def count_people(self) -> int:
        """Get the number of people"""
        query_result = await self.execute_read(count_people_nodes)
        return query_result[0]["count(p)"]

    async def find_person_by_id(self, person_id: str) -> PersonDataclass:
        """Find a person by its ID"""
        query_result = await self.execute_read(
            get_people_nodes_with_pagination,
            pagination=QueryPagination(limit=1, skip=0),
            person_id=person_id,
        )
        people = construct_people_list_from_query_result(query_result)
        if not people:
            raise NotFoundError(f"The person with uuid {person_id} was not found in the DB")
        return people[0]

    async def create_person(
        self, person_data: PersonUserInfo, uuid: str | None = None
    ) -> PersonDataclass:
        """Create a new person"""
        query_result = await self.execute_write(
            create_new_person_node, person_data=person_data, uuid=uuid
        )
        person_uuid: str = query_result[0]["p"]["uuid"]
        for parent in person_data.child_of:
            await self.execute_write(link_child_to_parent, parent_id=parent, child_id=person_uuid)
        for child in person_data.parent_of:
            await self.execute_write(link_child_to_parent, parent_id=person_uuid, child_id=child)
        for friend in person_data.friend_of:
            await self.execute_write(link_friends, person1_id=person_uuid, person2_id=friend)
        full_person = await self.find_person_by_id(person_id=person_uuid)
        return full_person

    async def update_person(self, person_data: PersonUserInfo, person_id: str) -> PersonDataclass:
        """Call mailing service to send email"""
        await self.delete_person(person_id=person_id)
        full_person = await self.create_person(person_data=person_data, uuid=person_id)
        return full_person

    async def delete_person(self, person_id: str) -> None:
        """Delete a person from id"""
        await self.execute_write(delete_one_person_query, person_id=person_id)

    async def get_ancestors_by_person_id(self, person_id: str) -> List[NameIdDataclass]:
        """Get the person ancestors"""
        query_result = await self.execute_write(get_ancestors_query, person_id=person_id)
        formatted_people = [
            NameIdDataclass(
                ID=person["ancestor"]["uuid"],
                name=f"{person['ancestor']['firstname']} {person['ancestor']['lastname']}",
            )
            for person in query_result
        ]
        return formatted_people

    async def get_family_fiends(self, person_id: str) -> List[NameIdDataclass]:
        """Get the person family friend"""
        query_result = await self.execute_write(get_family_friend, person_id=person_id)
        formatted_people = [
            NameIdDataclass(
                ID=person["friend"]["uuid"],
                name=f"{person['friend']['firstname']} {person['friend']['lastname']}",
            )
            for person in query_result
        ]
        return formatted_people

    async def execute_write(self, query_function, *args, **kwargs):
        """Wrap function execute write to raise a Neo4JError if any error occurs"""
        try:
            result = self.session.execute_write(query_function, *args, **kwargs)
        except Exception as error:
            raise Neo4JError(message=error.__repr__())
        return result

    async def execute_read(self, query_function, *args, **kwargs):
        """Wrap function execute read to raise a Neo4JError if any error occurs"""
        try:
            result = self.session.execute_read(query_function, *args, **kwargs)
        except Exception as error:
            raise Neo4JError(message=error.__repr__())
        return result
