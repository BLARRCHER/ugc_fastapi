from http import HTTPStatus

from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError

from db.user_info_db.database import get_session
from models.user_info import Bookmark, Like, Review


class BookmarkService:
    @staticmethod
    async def create(self, film_id: str, user_id: str, db: AsyncIOMotorClient = Depends(get_session)):
        collection = db["bookmarks"]
        bookmark = Bookmark(film_id=film_id, user_id=user_id)
        result = await collection.insert_one(bookmark.dict())
        return {"success": True, "id": str(result.inserted_id)}

    @staticmethod
    async def delete(self, film_id: str, user_id: str, db: AsyncIOMotorClient = Depends(get_session)):
        collection = db["bookmarks"]
        return collection.delete_one({"film_id": film_id, "user_id": user_id})

    @staticmethod
    async def get(self, user_id: str, db: AsyncIOMotorClient = Depends(get_session)):
        collection = db["bookmarks"]
        try:
            result = collection.find({"user_id": user_id})
        except Exception:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="find error")
        return [Bookmark(**doc) async for doc in result]


class LikeService:
    @staticmethod
    async def create(self, film_id:str, rating: int, user_id: str, db: AsyncIOMotorClient = Depends(get_session)):
        collection = db["likes"]

        try:
            model = dict(Like(film_id=film_id, user_id=user_id, rating=rating))
        except ValidationError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Error validation")

        try:
            await db["likes"].insert_one(model)
        except Exception:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Insert error")

    @staticmethod
    async def delete(self, film_id:str, user_id: str, db: AsyncIOMotorClient = Depends(get_session)):
        collection = db["likes"]
        await collection.delete_one({"film_id": film_id, "user_id": user_id})

    @staticmethod
    async def get(self, film_id: str, db: AsyncIOMotorClient = Depends(get_session)):
        collection = db["likes"]
        dislikes = await collection.count_documents({"film_id": film_id, "rating": 0})
        likes = await collection.count_documents({"film_id": film_id, "rating": 10})
        return dislikes, likes

    @staticmethod
    async def get_average(self, film_id: str, db: AsyncIOMotorClient = Depends(get_session)):
        collection = db["likes"]
        pipeline = [
            {"$match": {"film_id": film_id}},
            {"$group": {"_id": "$film_id", "average_rating": {"$avg": "$rating"}}},
        ]
        try:
            cursor = collection.aggregate(pipeline)
            result = await cursor.to_list(length=1)
        except Exception:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Find error")
        return result

    @staticmethod
    async def update(self, film_id: str, user_id: str, rating: int, db: AsyncIOMotorClient = Depends(get_session)):
        collection = db["likes"]
        if rating not in [0, 10]:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Рейтинг должен быть 0 или 10")
        try:
            result = await collection.update_one({"film_id": film_id, "user_id": user_id}, {"$set": {"rating": rating}})
        except Exception:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Update error")


class ReviewService:
    @staticmethod
    async def create(self, film_id: str, text: str, user_id: str, db: AsyncIOMotorClient = Depends(get_session)):
        collection = db["reviews"]
        review = Review(film_id=film_id, user_id=user_id, text=text)
        try:
            await collection.insert_one(review.dict())
        except Exception:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Insert error")
        return review

    @staticmethod
    async def get(
            self, query: dict,
            sort_dir: int, sort_field: str,
            db: AsyncIOMotorClient = Depends(get_session)
    ):
        collection = db["reviews"]
        try:
            cursor = collection.find(query).sort(sort_field, sort_dir)
        except Exception:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Find error")

        reviews = []
        for doc in await cursor.to_list(length=100):
            reviews.append(Review(**doc))
        return reviews
