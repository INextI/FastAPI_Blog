from core.models import User
from .shemas import UserBase, UserBaseFull, UserCreate

from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select
from sqlalchemy.engine import Result
from auth.security import hash_password

'''
async def create_user(user_in: UserCreate,
                      session: AsyncSession,
                      ) -> User:
    user: User = User(nickname = user_in.nickname, email = user_in.email, is_admin = user_in.is_admin, hashed_password = user_in.password)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
'''

async def get_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return users


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    stmt = select(User).filter(User.email == email)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user

async def create_user(user_in: UserCreate,
                      session: AsyncSession,
                      ) -> User:
    user: User = User(nickname = user_in.nickname,
                      is_admin = user_in.is_admin,
                      email = user_in.email,
                      hashed_password = hash_password(user_in.password)
                      )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    return await session.get(User, user_id)