from fastapi import APIRouter, Response, status

from app import crud
from app.api.deps import SessionDep
from app.core.exceptions import NotFoundException
from app.schemas.post import PostCreate, PostResponse, PostUpdate

router = APIRouter()


@router.get("", response_model=list[PostResponse])
async def list_posts(db: SessionDep, skip: int = 0, limit: int = 100) -> list[PostResponse]:
    posts = await crud.post.get_multi(db, skip=skip, limit=limit)
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: SessionDep) -> PostResponse:
    post = await crud.post.get(db, post_id)
    if post is None:
        raise NotFoundException("Post not found")
    return PostResponse.model_validate(post)


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post_in: PostCreate, owner_id: int, db: SessionDep) -> PostResponse:
    post = await crud.post.create(db, obj_in=post_in, owner_id=owner_id)
    return PostResponse.model_validate(post)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_in: PostUpdate, db: SessionDep) -> PostResponse:
    post = await crud.post.get(db, post_id)
    if post is None:
        raise NotFoundException("Post not found")
    post = await crud.post.update(db, db_obj=post, obj_in=post_in)
    return PostResponse.model_validate(post)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: SessionDep) -> Response:
    post = await crud.post.remove(db, record_id=post_id)
    if post is None:
        raise NotFoundException("Post not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
