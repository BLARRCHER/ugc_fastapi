from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from .services import ReviewService

from core.auth_bearer import AccessTokenPayload, jwt_bearer
from db.user_info_db.database import get_session
from models.user_info import Review

router = APIRouter()


@router.post("/{film_id}", response_model=Review, summary="Create review")
async def create_review(
    film_id: str,
    text: str,
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
    db: AsyncIOMotorClient = Depends(get_session)
):
    user_id = str(token_payload.sub)
    collection = db["reviews"]
    if await collection.find_one({"film_id": film_id, "user_id": user_id}):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Review already exist")

    return await ReviewService.create(film_id, text, user_id)


@router.get("/", response_model=list[Review], summary="Get review",
            description="Get review by film_id or user_id with sorting")
async def get_reviews(
    film_id: str = None,
    user_id: str = None,
    sort_by: str = "publication_date",
    ascending: bool = False
):
    query = {}
    if film_id:
        query["film_id"] = film_id
    if user_id:
        query["user_id"] = user_id

    sort_dir = 1 if ascending else -1
    sort_field = sort_by if sort_by in ["publication_date", "id"] else "publication_date"

    return await ReviewService.get(query, sort_field, sort_dir)
