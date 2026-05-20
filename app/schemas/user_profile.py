from pydantic import BaseModel, ConfigDict, Field


class UserProfileBase(BaseModel):
    bio: str | None = None
    avatar_url: str | None = Field(default=None, max_length=512)
    country: str | None = Field(default=None, max_length=100)


class UserProfileCreate(UserProfileBase):
    user_id: int


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfileResponse(UserProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
