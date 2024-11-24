
from typing import Optional, List
from datetime import date

from fastapi import HTTPException

from model.user_reponse import UserResponse
from model.user_request import UserRequest
from repository.database import database
from api.internalApi.model.user_answer_service_api import delete_answers_by_user_id

TABLE_NAME = "users"


async def get_by_id(user_id: int) -> Optional[UserResponse]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE id = :user_id"
    result = await database.fetch_one(query, values={"user_id": user_id})
    if result:
        return UserResponse(**result)
    return None


async def get_all() -> List[UserResponse]:
    query = f"SELECT * FROM {TABLE_NAME}"
    results = await database.fetch_all(query)
    return [UserResponse(**result) for result in results]


async def create_user(user: UserRequest) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} 
        (first_name, last_name, email, age, address)
        VALUES 
        (:first_name, :last_name, :email, :age, :address)
    """
    values = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "address": user.address,
    }

    await database.execute(query, values=values)
    last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    if last_record_id:
        return last_record_id[0]
    else:
        raise HTTPException(status_code=404, detail="Failed to retrieve last insert ID.")


async def update_user(user_id: int, user: UserRequest):
    query = f"""
        UPDATE {TABLE_NAME}
        SET first_name = :first_name,
            last_name = :last_name,
            email = :email,
            age = :age,
            address = :address
        WHERE id = :user_id
    """
    values = {
        "user_id": user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "address": user.address,
    }
    await database.execute(query, values=values)


async def delete_user(user_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE id = :user_id"
    result = await database.execute(query, values={"user_id": user_id})

    if result == 0:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    try:
        await delete_answers_by_user_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user's answers: {e}")

    return {"message": f"User with ID {user_id} and their answers were successfully deleted."}


async def register_user(user_id: int):
    if user_id is not None:
        query = f"""
            UPDATE {TABLE_NAME}
            SET is_registered = :is_registered,
                joining_date = :joining_date
            WHERE id = :user_id
        """
        values = {
            "user_id": user_id,
            "is_registered": True,
            "joining_date": date.today()
        }
        await database.execute(query=query, values=values)
    else:
        return None
