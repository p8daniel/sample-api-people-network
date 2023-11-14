from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class OffsetLimit:
    """Group the offset and the limit for a request"""

    offset: int
    limit: int


class QueryPagination(NamedTuple):
    """query parameters for pagination in the query"""

    limit: int
    skip: int
