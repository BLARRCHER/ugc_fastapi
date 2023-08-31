from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from core.auth_bearer import AccessTokenPayload, jwt_bearer
from db.user_info_db.database import get_session
from models.user_info import Bookmark
from .services import BookmarkService

router = APIRouter()


@router.post("/{film_id}", summary="Create bookmark", description="Create bookmark to especially film")
async def create_bookmark(
    film_id: str,
    db: AsyncIOMotorClient = Depends(get_session),
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
):
    collection = db["bookmarks"]
    user_id = str(token_payload.sub)

    if await collection.find_one({"film_id": film_id, "user_id": user_id}):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Bookmark already exist")
    try:
        result = await BookmarkService.create(film_id, user_id)
        return result
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Insert error")


@router.delete("/{film_id}", summary="Delete bookmark", description="Delete bookmark by id")
async def delete_bookmark(
    film_id: str,
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
):
    user_id = str(token_payload.sub)
    try:
        result = await BookmarkService.delete(film_id, user_id)
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Delete error")

    if result.deleted_count == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Закладка не найдена")
    return {"deleted": film_id}


@router.get("/", response_model=list[Bookmark], summary="Get bookmarks", description="Get all users bookmarks")
async def get_bookmarks(
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
):
    user_id = str(token_payload.sub)
    return await BookmarkService.get(user_id)
