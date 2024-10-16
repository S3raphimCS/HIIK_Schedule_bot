from typing import List, Optional, Tuple

from create_bot import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from utils.consts import DIRECTION_CHOICES

from .base import connection
from .models import Change, User


@connection
async def set_user(session, tg_id: int) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            new_user = User(id=tg_id)
            session.add(new_user)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return user
    except SQLAlchemyError as err:
        logger.error(f"Ошибка при добавлении пользователя: {err}")
        await session.rollback()


@connection
async def change_user_direction(session, tg_id: int, direction: str) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            logger.error(f"Пользователь с ID {tg_id} не найден.")
            return None

        user.agreement = True
        user.direction = direction

        await session.commit()
        logger.info(f"Пользователь {tg_id} подписался на рассылку {direction}")
        return user
    except SQLAlchemyError as err:
        logger.error(f"Ошибка при обновлении данных рассылки пользователя {tg_id}: {err}")
        await session.rollback()


@connection
async def disable_agreement(session, tg_id: int) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            logger.error(f"Пользователь с ID {tg_id} не найден.")
            return None

        user.agreement = False
        direction = user.direction
        await session.commit()
        logger.info(f"Пользователь {tg_id} отписался от рассылки {direction}")
        return user

    except SQLAlchemyError as err:
        logger.error(f"Ошибка при обновлении данных рассылки пользователя {tg_id}: {err}")
        await session.rollback()


@connection
async def enable_agreement(session, tg_id: int) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            logger.error(f"Пользователь с ID {tg_id} не найден.")
            return None

        user.agreement = True
        direction = user.direction
        await session.commit()
        logger.info(f"Пользователь {tg_id} возобновил рассылку на {direction}")
        return user

    except SQLAlchemyError as err:
        logger.error(f"Ошибка при обновлении данных рассылки пользователя {tg_id}: {err}")
        await session.rollback()


@connection
async def disable_direction(session, tg_id: int) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            logger.error(f"Пользователь с ID {tg_id} не найден.")
            return None

        user.agreement = False
        user.direction = None

        await session.commit()
        logger.info(f"Пользователь {tg_id} убрал направление")
        return user

    except SQLAlchemyError as err:
        logger.error(f"Ошибка при обновлении данных рассылки пользователя {tg_id}: {err}")
        await session.rollback()


@connection
async def get_changes_or_create(session, title: str, link: str) -> Tuple[str, str] | None:
    try:
        change = await session.scalar(select(Change).filter_by(title=title))

        if not change:
            direction = title.split()[-1]
            change = Change(title=title, direction=DIRECTION_CHOICES[direction], link=link)
            session.add(change)
            change = (change.title, change.link)
            await session.commit()
            logger.info(f"Создана запись изменения расписания '{title}'")
            return change
        else:
            logger.info(f"Было проверено существующее изменение {title}")
            return None
    except SQLAlchemyError as err:
        logger.error(f"При парсинге изменения возникла ошибка: {err}")
        session.rollback()

@connection
async def get_users_with_agreement(session, direction: str) -> List[str]:
    try:
        users = await session.scalars(select(User).filter_by(agreement=True).filter_by(direction=DIRECTION_CHOICES[direction]))
        users_id = [str(i.id) for i in users.all()]
        await session.commit()
        logger.info("Студенты ВО успешно прошли выборку")
        return users_id
    except SQLAlchemyError as err:
        logger.error(f"Ошибка выборки студентов {direction}: {err}")

@connection
async def get_last_changes_query(session, tg_id: int) -> Tuple[str, str] | None:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            logger.error(f"Пользователь с ID {tg_id} не найден.")
            return None

        if not user.direction:
            logger.warning(f"Пользователь с ID {tg_id} попытался получить последнее изменение без выбранного направления")
            return None
        else:
            changes = await session.scalars(select(Change).filter_by(direction=user.direction))
            changes = changes.all()
            title = changes[-1].title
            link = changes[-1].link
            return title, link

    except SQLAlchemyError as err:
        logger.error(f"Ошибка получения последних изменений: {err}")