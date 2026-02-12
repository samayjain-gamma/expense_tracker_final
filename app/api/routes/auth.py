from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.users import Token, UserLogin, UserNew, UserResponse

router = APIRouter()


@router.post(
    "/register",
    operation_id="register",
    description="Registration of User",
    response_model=UserResponse,
)
async def register(user_in: UserNew, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = hash_password(user_in.password)
    user = User(
        username=user_in.username, email=user_in.email, password_hash=hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return UserResponse(user_id=user.user_id, username=user.username, email=user.email)


@router.post(
    "/login", operation_id="login", description="User login", response_model=Token
)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    valid_pwd = verify_password(user_in.password, user.password_hash)

    if not valid_pwd:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    token = create_access_token({"user_id": user.user_id, "email": user.email})

    return {"access_token": token, "token_type": "bearer"}
