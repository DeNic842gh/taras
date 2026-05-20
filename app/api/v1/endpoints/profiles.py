from fastapi import APIRouter, status

from app import crud
from app.api.deps import SessionDep
from app.core.exceptions import ConflictException, NotFoundException
from app.schemas.user_profile import UserProfileCreate, UserProfileResponse, UserProfileUpdate

router = APIRouter()


@router.get("", response_model=list[UserProfileResponse])
async def list_profiles(
    db: SessionDep, skip: int = 0, limit: int = 100
) -> list[UserProfileResponse]:
    profiles = await crud.user_profile.get_multi(db, skip=skip, limit=limit)
    return [UserProfileResponse.model_validate(p) for p in profiles]


@router.get("/by-user/{user_id}", response_model=UserProfileResponse)
async def get_profile_by_user(user_id: int, db: SessionDep) -> UserProfileResponse:
    profile = await crud.user_profile.get_by_user_id(db, user_id)
    if profile is None:
        raise NotFoundException("Profile not found")
    return UserProfileResponse.model_validate(profile)


@router.get("/{profile_id}", response_model=UserProfileResponse)
async def get_profile(profile_id: int, db: SessionDep) -> UserProfileResponse:
    profile = await crud.user_profile.get(db, profile_id)
    if profile is None:
        raise NotFoundException("Profile not found")
    return UserProfileResponse.model_validate(profile)


@router.post("", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(profile_in: UserProfileCreate, db: SessionDep) -> UserProfileResponse:
    existing = await crud.user_profile.get_by_user_id(db, profile_in.user_id)
    if existing is not None:
        raise ConflictException("Profile for this user already exists")
    profile = await crud.user_profile.create(db, obj_in=profile_in)
    return UserProfileResponse.model_validate(profile)


@router.put("/{profile_id}", response_model=UserProfileResponse)
async def update_profile(
    profile_id: int, profile_in: UserProfileUpdate, db: SessionDep
) -> UserProfileResponse:
    profile = await crud.user_profile.get(db, profile_id)
    if profile is None:
        raise NotFoundException("Profile not found")
    profile = await crud.user_profile.update(db, db_obj=profile, obj_in=profile_in)
    return UserProfileResponse.model_validate(profile)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(profile_id: int, db: SessionDep) -> None:
    profile = await crud.user_profile.remove(db, record_id=profile_id)
    if profile is None:
        raise NotFoundException("Profile not found")
