import re
from dataclasses import dataclass
from typing import Annotated, Any, Dict, List

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field


def to_camel(string: str) -> str:
    """Convert a string from snake_case to lowerCamel case"""
    return re.sub(r"_([a-z])", lambda match: r"{}".format(match.group(1).upper()), string)


class CamelModel(BaseModel):
    """Set snake case to camel conversion in payload"""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class PayloadModel(CamelModel):
    """Generic payload model"""

    data: List[Any] | Dict[str, Any] | BaseModel
    meta: Any | None = None


@dataclass
class PaginationParams:
    """Group the pagination parameters"""

    page_number: int
    page_size: int


async def get_pagination_params(
    page_number: Annotated[int, Query(alias="page[number]", ge=0)] = 0,
    page_size: Annotated[int, Query(alias="page[size]", gt=0, le=100)] = 10,
) -> PaginationParams:
    """Create pagination parameters object from query parameters"""
    return PaginationParams(page_number=page_number, page_size=page_size)


class PaginationDetails(BaseModel):
    """Model for pagination details"""

    page_number: int = Field(alias="page[number]")
    page_size: int = Field(alias="page[size]")
    page_total: int = Field(alias="page[total]")

    model_config = ConfigDict(populate_by_name=True)


class PaginationModel(BaseModel):
    """Model for pagination payload"""

    pagination: PaginationDetails
