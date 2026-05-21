from fastapi import APIRouter, status

from app import crud
from app.api.deps import CurrentUserDep, SessionDep
from app.core.exceptions import ForbiddenException, NotFoundException
from app.schemas.post import PostCreate, PostResponse, PostUpdate

router = APIRouter()


@router.get("", response_model=list[PostResponse])
async def list_posts(
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> list[PostResponse]:
    posts = await crud.post.get_multi(db, skip=skip, limit=limit)
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/me", response_model=list[PostResponse])
async def list_my_posts(
    db: SessionDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 100,
) -> list[PostResponse]:
    """Protected: posts created by the current user."""
    posts = await crud.post.get_by_owner(db, current_user.id, skip=skip, limit=limit)
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: SessionDep) -> PostResponse:
    post = await crud.post.get(db, post_id)
    if post is None:
        raise NotFoundException("Post not found")
    return PostResponse.model_validate(post)


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_in: PostCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> PostResponse:
    """Protected: create a post as the authenticated user."""
    post = await crud.post.create(db, obj_in=post_in, owner_id=current_user.id)
    return PostResponse.model_validate(post)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> PostResponse:
    """Protected: only the post owner may update."""
    post = await crud.post.get(db, post_id)
    if post is None:
        raise NotFoundException("Post not found")
    if post.owner_id != current_user.id:
        raise ForbiddenException("Not allowed to edit this post")
    post = await crud.post.update(db, db_obj=post, obj_in=post_in)
    return PostResponse.model_validate(post)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> None:
    """Protected: only the post owner may delete."""
    post = await crud.post.get(db, post_id)
    if post is None:
        raise NotFoundException("Post not found")
    if post.owner_id != current_user.id:
        raise ForbiddenException("Not allowed to delete this post")
    await crud.post.remove(db, record_id=post_id)
