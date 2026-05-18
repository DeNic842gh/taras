from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

# OAuth2 / JWT: async def get_current_user(...) -> User: ...

SessionDep = Annotated[AsyncSession, Depends(get_db)]
