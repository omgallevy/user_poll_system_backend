from typing import List

from fastapi import APIRouter, HTTPException
from model.user import User
from model.user_reponse import UserResponse
from model.user_request import UserRequest
from service import user_service

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")
    return user


@router.post("/")
async def create_user(user: UserRequest):
    try:
        user_id = await user_service.create_user(user)
        created_user = await user_service.get_by_id(user_id)
        return created_user
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=404, detail=f"Can't create new user")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserRequest):
    existing_user = await user_service.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"Can't update user with id: {user_id}, user not found")

    await user_service.update_user(user_id, user)
    updated_user = await user_service.get_by_id(user_id)
    return updated_user


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int):
    user = await user_service.delete_user(user_id)
    return user


@router.get("/", response_model=List[UserResponse])
async def get_users():
    return await user_service.get_all()


@router.put('/register/{user_id}', response_model=UserResponse)
async def register_user(user_id: int):
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_registered:
        raise HTTPException(status_code=400, detail=f"User with id: {user_id} is already registered.")

    await user_service.register_user(user_id)
    updated_user = await user_service.get_by_id(user_id)
    return updated_user
