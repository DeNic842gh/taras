from fastapi import APIRouter, Response, status

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.storage.user_memory import user_memory_store

router = APIRouter()


def _to_response(user: dict) -> UserResponse:
    return UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user.get("full_name"),
        is_active=user.get("is_active", True),
    )


@router.get("", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 100) -> list[UserResponse]:
    users = user_memory_store.list_users(skip=skip, limit=limit)
    return [_to_response(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    user = user_memory_store.get_user(user_id)
    return _to_response(user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate) -> UserResponse:
    user = user_memory_store.create_user(user_in)
    return _to_response(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_in: UserUpdate) -> UserResponse:
    user = user_memory_store.update_user(user_id, user_in)
    return _to_response(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int) -> Response:
    user_memory_store.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
