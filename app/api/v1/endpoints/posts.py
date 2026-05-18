from fastapi import APIRouter

from app import crud
from app.api.deps import SessionDep
from app.core.exceptions import NotFoundException
from app.schemas.post import PostCreate, PostResponse

router = APIRouter()


@router.get("", response_model=list[PostResponse])
async def list_posts(
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> list[PostResponse]:
    posts = await crud.post.get_multi(db, skip=skip, limit=limit)
    return [PostResponse.model_validate(p) for p in posts]


@router.post("", response_model=PostResponse, status_code=201)
async def create_post(
    post_in: PostCreate,
    owner_id: int,
    db: SessionDep,
) -> PostResponse:
    post = await crud.post.create(db, obj_in=post_in, owner_id=owner_id)
    return PostResponse.model_validate(post)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: SessionDep,
) -> PostResponse:
    post = await crud.post.get(db, post_id)
    if post is None:
        raise NotFoundException("Post not found")
    return PostResponse.model_validate(post)
