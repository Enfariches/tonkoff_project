import sqlite3 as sq
import aiosqlite

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Profile, CheckUser, Message
from sqlalchemy import select, update


async def create_check_user(session: AsyncSession, user_id):

    user = await session.execute(select(CheckUser).where(CheckUser.user_id == user_id))
    if user.fetchone() is None:
        new_user = CheckUser(
            user_id=user_id,
        )
        session.add(new_user)
        await session.commit()
    await session.close()


async def create_profile(session: AsyncSession, user_id, user_username, payload):

    user = await session.execute(select(Profile).where(Profile.user_id == user_id))
    if user.fetchone() is None:
        new_user = Profile(
            user_id=user_id,
            user_username=user_username,
            payload=payload
        )
        session.add(new_user)
        if payload != None:
            await session.execute(update(Profile).values(count_invited=Profile.count_invited + 1).where(Profile.user_id == payload))
        await session.commit()
    await session.close()


async def update_link_profile(session: AsyncSession, user_id, ref_link):

    query = update(Profile).where(Profile.user_id == user_id).values(
        ref_link = ref_link
    )
    await session.execute(query)
    await session.commit()


async def get_field(session: AsyncSession, user_id, name_field):

    field = await session.execute(select(getattr(Profile, name_field)).where(Profile.user_id == user_id))
    field = field.fetchone()[0]
    await session.close()
    return field

async def status_check(session: AsyncSession, user_id, name_field):

    check = await session.execute(select(getattr(CheckUser, name_field)).where(CheckUser.user_id == user_id))
    check_status = check.fetchone()[0]
    await session.close()
    return check_status

async def update_check(session: AsyncSession, user_id, name_field):

    query = update(CheckUser).where(CheckUser.user_id == user_id).values(**{name_field: True})
    await session.execute(query)
    await session.commit()


async def update_friends_score(session: AsyncSession, user_id):

    query_friend = await session.execute(select(Profile.user_score).where(Profile.payload == user_id))
    if query_friend.fetchone() is not None:
        query = update(Profile.friends_score).where(Profile.user_id == user_id).values(query_friend.fetchone()[0])
        await session.execute(query)
        await session.commit()
    await session.close()


async def get_invited_users(session: AsyncSession, user_id):

    query_friends = await session.execute(select(Profile.user_username, Profile.total).where(Profile.payload == user_id))
    if query_friends.fetchall() is not None:
        lst_friend = [(user[0], user[1]) for user in query_friends.fetchall()]
        await session.close()
        return lst_friend
    await session.close()

async def update_wallet_address(session: AsyncSession, user_id, wallet_address):

    await session.execute(update(Profile).values(wallet_address = wallet_address).where(Profile.user_id == user_id))
    await session.commit()

async def get_top_50_users(session: AsyncSession):
    query = await session.execute(select(Profile.user_username, Profile.total).order_by(Profile.total).limit(50))
    result = query.fetchall()
    await session.close()
    return result

async def get_all_user_ids(session: AsyncSession):

    query = await session.execute(select(Profile.user_id))
    result = [row[0] for row in query.fetchall()]
    await session.close()
    return result

async def create_message(session: AsyncSession, user_id):

    user = await session.execute(select(Message).where(Message.user_id == user_id))
    if user.fetchone() is None:
        new_user = Message(
            user_id=user_id,          
        )
        session.add(new_user)
        await session.commit()
    await session.close()

async def update_message(session, user_id, admin_message):

    await session.execute(update(Message).values(admin_message = admin_message).where(Message.user_id == user_id))
    await session.commit()

async def get_message(session: AsyncSession, user_id):

    field = await session.execute(select(Message.admin_message).where(Message.user_id == user_id))
    field = field.fetchone()[0]
    await session.close()
    return field

async def update_balance(session: AsyncSession, user_id, profit):

    await session.execute(update(Profile).values(balance=Profile.balance + profit).where(Profile.user_id == user_id))
    await session.commit()

async def update_friends_balance(session: AsyncSession, user_id):

    query_friend = await session.execute(select(Profile.balance).where(Profile.payload == user_id))
    if query_friend.fetchone() is not None:
        query = update(Profile.friends_balance).where(Profile.user_id == user_id).values(query_friend.fetchone[0])
        await session.execute(query)
        await session.commit()
    await session.close()

async def update_total(session: AsyncSession, user_id, total):

    await session.execute(update(Profile).values(total = total).where(Profile.user_id == user_id))
    await session.commit()











