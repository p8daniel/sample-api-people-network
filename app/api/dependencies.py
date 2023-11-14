from typing import Generator

from app.core.db_connection import NEO4J_CONNECTION
from app.dao.people.interface import PeopleNeo4JDAO


async def get_db_interface() -> Generator:
    """Inject the neo4j interface as database interface"""
    with NEO4J_CONNECTION.driver.session() as session:
        yield PeopleNeo4JDAO(db_session=session)
