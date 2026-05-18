from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def login() -> dict[str, str]:
    """Placeholder: implement JWT login with app.core.security."""
    return {"detail": "Not implemented yet"}
