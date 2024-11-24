from typing import Optional, List

from model.user_reponse import UserResponse
from model.user_request import UserRequest
from repository import user_repository


async def get_by_id(user_id: int) -> Optional[UserResponse]:
    return await user_repository.get_by_id(user_id)


async def get_all() -> List[UserResponse]:
    return await user_repository.get_all()


async def create_user(user: UserRequest) -> int:
    return await user_repository.create_user(user)


async def update_user(user_id: int, user: UserRequest) -> UserResponse:
    existing_user = await user_repository.get_by_id(user_id)
    if existing_user is not None:
        await user_repository.update_user(user_id, user)
        return await user_repository.get_by_id(user_id)
    else:
        raise Exception(f"Can't update user with id {user_id}, id is not existing")


async def delete_user(user_id: int):
    user = await user_repository.get_by_id(user_id)
    if user:
        await user_repository.delete_user(user_id)
        return user
    else:
        raise Exception(f"User with ID {user_id} and their answers were successfully deleted.")


async def register_user(user_id: int) -> UserResponse:
    user = await user_repository.get_by_id(user_id)
    if user:
        if not user.is_registered:
            await user_repository.register_user(user_id)
            return await get_by_id(user_id)
        else:
            raise Exception(f"User with id {user_id} is already registered")
    else:
        raise Exception(f"User with id {user_id} not found")
