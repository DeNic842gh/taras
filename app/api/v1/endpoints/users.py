from fastapi import APIRouter, Response, status

from app import crud
from app.api.deps import CurrentUserDep, SessionDep
from app.core.config import settings
from app.core.exceptions import ConflictException, NotFoundException
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.storage.user_memory import user_memory_store

router = APIRouter()


def _memory_to_response(user: dict) -> UserResponse:
    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        full_name=user.get("full_name"),
        is_active=user.get("is_active", True),
    )


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: CurrentUserDep) -> UserResponse:
    """Protected: profile of the logged-in user."""
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_in: UserUpdate,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> UserResponse:
    """Protected: update own profile (not is_active)."""
    if user_in.is_active is not None:
        user_in = user_in.model_copy(update={"is_active": None})
    if user_in.username and user_in.username != current_user.username:
        existing = await crud.user.get_by_username(db, user_in.username)
        if existing and existing.id != current_user.id:
            raise ConflictException("Username already taken")
    if user_in.email and str(user_in.email) != current_user.email:
        existing = await crud.user.get_by_email(db, str(user_in.email))
        if existing and existing.id != current_user.id:
            raise ConflictException("Email already registered")
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
async def list_users(
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> list[UserResponse]:
    if settings.use_memory_store:
        return [_memory_to_response(u) for u in user_memory_store.list_users(skip, limit)]
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: SessionDep) -> UserResponse:
    if settings.use_memory_store:
        return _memory_to_response(user_memory_store.get_user(user_id))
    user = await crud.user.get(db, user_id)
    if user is None:
        raise NotFoundException("User not found")
    return UserResponse.model_validate(user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: SessionDep) -> UserResponse:
    if settings.use_memory_store:
        return _memory_to_response(user_memory_store.create_user(user_in))
    if await crud.user.get_by_email(db, str(user_in.email)):
        raise ConflictException("Email already registered")
    if await crud.user.get_by_username(db, user_in.username):
        raise ConflictException("Username already taken")
    user = await crud.user.create(db, obj_in=user_in)
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: SessionDep,
) -> UserResponse:
    if settings.use_memory_store:
        return _memory_to_response(user_memory_store.update_user(user_id, user_in))
    user = await crud.user.get(db, user_id)
    if user is None:
        raise NotFoundException("User not found")
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: SessionDep) -> Response:
    if settings.use_memory_store:
        user_memory_store.delete_user(user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    user = await crud.user.remove(db, record_id=user_id)
    if user is None:
        raise NotFoundException("User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
