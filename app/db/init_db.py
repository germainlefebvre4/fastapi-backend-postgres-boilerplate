from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings


def init_db(db: Session) -> None:
    user = crud.user.get_by_email(db, email=settings.USER_ADMIN_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.USER_ADMIN_EMAIL,
            firstname=settings.USER_ADMIN_FIRSTNAME,
            password=settings.USER_ADMIN_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)

    user = crud.user.get_by_email(db, email=settings.USER_TEST_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.USER_TEST_EMAIL,
            firstname=settings.USER_TEST_FIRSTNAME,
            password=settings.USER_TEST_PASSWORD,
            is_superuser=False,
        )
        user = crud.user.create(db, obj_in=user_in)
    