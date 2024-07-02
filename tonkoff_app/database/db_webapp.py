import sqlite3
from datetime import datetime
from database.engine import session_maker
from sqlalchemy import select, update
from database.models import Profile

async def get_user_score(user_id):

    async with session_maker() as session:
        user = await session.execute(select(Profile.user_score).where(Profile.user_id == user_id))
        result = user.fetchone()[0]
        return result

async def update_score(user_id, new_score):

    async with session_maker() as session:
        await session.execute(update(Profile).where(Profile.user_id == user_id).values(user_score=new_score))
        await session.commit()

async def get_last_reset_time(user_id):

    async with session_maker() as session:
        time = await session.execute(select(Profile.last_reset_time).where(Profile.user_id == user_id))
        result = time.fetchone()[0]
        return result

async def update_last_reset_time(user_id, reset_time):

    async with session_maker() as session:
        await session.execute(update(Profile).where(Profile.user_id == user_id).values(last_reset_time=reset_time))
        await session.commit()

