from fastapi import APIRouter, Response, status

from app.api.deps import SessionDep
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()


@router.get("", response_model=list[UserResponse])
async def list_users(db: SessionDep, skip: int = 0, limit: int = 100) -> list[UserResponse]:
    return await user_service.list_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: SessionDep) -> UserResponse:
    return await user_service.get_user(db, user_id)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: SessionDep) -> UserResponse:
    return await user_service.create_user(db, user_in)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_in: UserUpdate, db: SessionDep) -> UserResponse:
    return await user_service.update_user(db, user_id, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: SessionDep) -> Response:
    await user_service.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
