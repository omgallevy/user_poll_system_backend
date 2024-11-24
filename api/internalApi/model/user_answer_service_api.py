import httpx
from typing import Optional
from api.internalApi.model.user_answer_response import UserAnswerResponse
from config.config import Config

config = Config()


async def get_answers_by_user_id(answer_id: int) -> Optional[UserAnswerResponse]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{config.USER_ANSWER_SERVICE_BASE_URL}/{answer_id}")
        if response.status_code == 200:
            return UserAnswerResponse(**response.json())
        else:
            return None


async def delete_answers_by_user_id(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{config.USER_ANSWER_SERVICE_BASE_URL}/user/{user_id}")
        if response.status_code != 200:
            response.raise_for_status()
