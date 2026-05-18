import hashlib
from threading import Lock

from app.core.exceptions import ConflictException, NotFoundException
from app.schemas.user import UserCreate, UserUpdate


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

_lock = Lock()
_users: dict[int, dict] = {}
_next_id = 1


class UserMemoryStore:
    """In-memory user storage (dict emulation) for Lab 3."""

    def list_users(self, skip: int = 0, limit: int = 100) -> list[dict]:
        with _lock:
            items = list(_users.values())
        return items[skip : skip + limit]

    def get_user(self, user_id: int) -> dict:
        with _lock:
            user = _users.get(user_id)
        if user is None:
            raise NotFoundException("User not found")
        return user

    def create_user(self, user_in: UserCreate) -> dict:
        global _next_id
        with _lock:
            for existing in _users.values():
                if existing["email"] == str(user_in.email).lower():
                    raise ConflictException("User with this email already exists")

            user_id = _next_id
            _next_id += 1
            record = {
                "id": user_id,
                "email": str(user_in.email).lower(),
                "full_name": user_in.full_name,
                "is_active": user_in.is_active,
                "hashed_password": _hash_password(user_in.password),
            }
            _users[user_id] = record
        return record

    def update_user(self, user_id: int, user_in: UserUpdate) -> dict:
        with _lock:
            user = _users.get(user_id)
            if user is None:
                raise NotFoundException("User not found")

            update_data = user_in.model_dump(exclude_unset=True)
            if "email" in update_data and update_data["email"] is not None:
                email = str(update_data["email"]).lower()
                for uid, existing in _users.items():
                    if uid != user_id and existing["email"] == email:
                        raise ConflictException("User with this email already exists")
                user["email"] = email

            if "full_name" in update_data:
                user["full_name"] = update_data["full_name"]
            if "is_active" in update_data:
                user["is_active"] = update_data["is_active"]
            if "password" in update_data and update_data["password"] is not None:
                user["hashed_password"] = _hash_password(update_data["password"])

            _users[user_id] = user
        return user

    def delete_user(self, user_id: int) -> None:
        with _lock:
            if user_id not in _users:
                raise NotFoundException("User not found")
            del _users[user_id]

    def count(self) -> int:
        with _lock:
            return len(_users)

    def reset(self) -> None:
        global _next_id
        with _lock:
            _users.clear()
            _next_id = 1


user_memory_store = UserMemoryStore()
