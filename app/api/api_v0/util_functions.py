from app.api.api_v0.models.common import PaginationParams
from app.models.common import OffsetLimit


def pagination_to_offset_limit(pagination: PaginationParams) -> OffsetLimit:
    """Convert pagination into offset and limit"""
    return OffsetLimit(
        limit=pagination.page_size, offset=pagination.page_size * pagination.page_number
    )
