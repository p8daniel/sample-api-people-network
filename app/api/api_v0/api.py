from fastapi import APIRouter

from app.api.api_v0.endpoints import people, people_relationship

api_router = APIRouter()
api_router.include_router(people.router, prefix="/people", tags=["People"])
api_router.include_router(
    people_relationship.router, prefix="/people", tags=["PeopleRelationship"]
)
