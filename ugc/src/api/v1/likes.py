from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from .services import LikeService

from core.auth_bearer import AccessTokenPayload, jwt_bearer
from db.user_info_db.database import get_session


router = APIRouter()


@router.post(
    "/{film_id}",
    summary="Add like to storage",
    description="Add rating 0/10 to storage",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.CREATED,
)
async def add_like(
    film_id: str,
    rating: int,
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
    db: AsyncIOMotorClient = Depends(get_session),
):
    user_id = str(token_payload.sub)
    if await db["likes"].find_one({"film_id": film_id, "user_id": user_id}):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Like already exist")
    await LikeService.create(film_id, rating, user_id)
    return "created"


@router.delete(
    "/{film_id}",
    summary="Delete like",
    description="Delete like by id",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.OK,
)
async def delete_like(film_id: str, token_payload: AccessTokenPayload = Depends(jwt_bearer)):
    user_id = str(token_payload.sub)

    try:
        result = await LikeService.delete(film_id, user_id)
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Delete error")

    if result.deleted_count > 0:
        return {"message": "Лайк успешно удален"}

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Лайк не найден")


@router.get(
    "/{film_id}",
    summary="Get likes and dislikes",
    description="Get likes and dislikes from film_id",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.OK,
)
async def get_rating(film_id: str):
    try:
        dislikes, likes = await LikeService.get(film_id)
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Find error")

    return likes, dislikes


@router.get(
    "/average_rating/{film_id}",
    summary="Get average rating",
    description="Get average rating from film_id",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.OK,
)
async def get_average_rating(film_id: str):
    result = await LikeService.get_average(film_id)

    if result:
        return result

    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Not result")


@router.put(
    "/{film_id}",
    summary="Update rating",
    description="Update rating from film_id",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.OK,
)
async def update_rating(
    film_id: str,
    rating: int,
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
):
    user_id = str(token_payload.sub)
    result = await LikeService.update(film_id, user_id, rating)

    if result.modified_count > 0:
        return {"message": "Лайк успешно обновлен"}

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Лайк не найден")
