import logging

from app.core.environment import settings
from app.dp.connection import Neo4jConnection

logger = logging.getLogger(__name__)


NEO4J_CONNECTION = Neo4jConnection(
    settings.NEO4J_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD
)
logger.info("Connection to neo4j initialized")


async def close_neo4j_connection() -> None:
    """Close application connection to neo4j"""
    NEO4J_CONNECTION.close()
    logger.info("Connection to neo4j closed")
