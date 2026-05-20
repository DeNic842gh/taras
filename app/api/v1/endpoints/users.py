from fastapi import APIRouter, Response, status

from app import crud
from app.api.deps import SessionDep
from app.core.exceptions import NotFoundException
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.get("", response_model=list[UserResponse])
async def list_users(db: SessionDep, skip: int = 0, limit: int = 100) -> list[UserResponse]:
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: SessionDep) -> UserResponse:
    user = await crud.user.get(db, user_id)
    if user is None:
        raise NotFoundException("User not found")
    return UserResponse.model_validate(user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: SessionDep) -> UserResponse:
    user = await crud.user.create(db, obj_in=user_in)
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_in: UserUpdate, db: SessionDep) -> UserResponse:
    user = await crud.user.get(db, user_id)
    if user is None:
        raise NotFoundException("User not found")
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: SessionDep) -> Response:
    user = await crud.user.remove(db, record_id=user_id)
    if user is None:
        raise NotFoundException("User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
