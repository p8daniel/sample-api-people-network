from __future__ import annotations

from types import TracebackType
from typing import Type

from neo4j import Driver, GraphDatabase


class Neo4jConnection:
    """Manage Neo4j connection"""

    def __init__(self, uri: str, username: str, password: str) -> None:
        if username or password:
            self._driver = GraphDatabase.driver(uri, auth=(username, password))
        else:
            self._driver = GraphDatabase.driver(uri)

    def close(self) -> None:
        """Clone neo4j client"""
        self._driver.close()

    def __enter__(self) -> Neo4jConnection:
        return self

    def __aenter__(self) -> Neo4jConnection:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    @property
    def driver(self) -> Driver:
        """Return the neo4j driver"""
        return self._driver
