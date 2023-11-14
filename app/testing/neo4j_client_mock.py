from contextlib import contextmanager
from typing import List

from app.models.common import QueryPagination
from app.models.peoples import NameIdDataclass, PersonDataclass, PersonUserInfo


@contextmanager
class TestGraphDatabaseSession:
    """Class Session for testing"""

    def execute_read(self):
        """Execute read"""
        ...

    def execute_write(self):
        """Execute write"""
        ...


class TestDBInterface:
    """Repository interface for peoples"""

    async def get_people_paginated(self, pagination: QueryPagination) -> List[PersonDataclass]:
        """Get people function"""
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
