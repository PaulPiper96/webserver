from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.schema import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


# -------------------------------------------------
# DB Dependency
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(session=db)


# -------------------------------------------------
# Routes
# -------------------------------------------------
@router.post("/", response_model=UserRead, status_code=201)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(payload)


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[UserRead])
def list_users(
    service: UserService = Depends(get_user_service),
):
    return service.list_users()