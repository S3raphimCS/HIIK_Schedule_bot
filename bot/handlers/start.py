from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from create_bot import admins, bot
from data_base.queries import (change_user_direction, disable_agreement,
                               disable_direction, enable_agreement,
                               get_changes_or_create, get_last_changes_query,
                               get_users_with_agreement, set_user)
from keyboards.all_kb import (change_kb_with_disable, change_kb_with_enable,
                              start_kb)
from sqlalchemy.exc import SQLAlchemyError
from utils.changes_request import parse

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await set_user(tg_id=message.from_user.id)

    await message.answer(
        "Привет! Я бот расписания ХИИК.\n"
        "Вам необходимо выбрать на клавиатуре ступень вашего образования.",
        reply_markup=start_kb(message.from_user.id))


@router.message(F.text.contains("профессиональное"))
async def choose_vo_direction(message: Message):
    await change_user_direction(tg_id=message.from_user.id, direction=message.text[2:])
    await message.answer(
        f"Вы успешно подписались на рассылку изменения расписания {message.text[2:]}.\n"
        f"Вам начнут приходить изменения со следующего дня.\n"
        f"Для отмены или изменения направления выберите необходимые кнопки на клавиатуре.",
        reply_markup=change_kb_with_disable(message.from_user.id))


@router.message(F.text.contains("Обратная связь"))
async def feedback(message: Message):
    await message.answer("Ссылка для обратной связи c разработчиком - https://t.me/S3raphimCS")


@router.message(F.text.contains("Отменить рассылку"))
async def cancel_mailing(message: Message):
    user = await disable_agreement(tg_id=message.from_user.id)
    if user:
        await message.answer("Рассылка была отменена", reply_markup=change_kb_with_enable(message.from_user.id))
    else:
        await message.answer("Ошибка в отмене рассылки")


@router.message(F.text.contains("Изменить направление"))
async def change_mailing(message: Message):
    await disable_direction(tg_id=message.from_user.id)
    await message.answer("Рассылка была выключена.\n"
                         "Вновь выберите направление, чтобы вернуть рассылку",
                         reply_markup=start_kb(message.from_user.id))


@router.message(F.text.contains("Включить рассылку"))
async def enable_mailing(message: Message):
    await enable_agreement(tg_id=message.from_user.id)
    await message.answer("Рассылка вновь подключена", reply_markup=change_kb_with_disable(message.from_user.id))


@router.message(F.text.contains("Получить последние изменения"))
async def get_last_changes(message: Message):
    user_id = message.from_user.id
    title, link = await get_last_changes_query(user_id)
    await message.answer(f"{title}\n{link}")


@router.message(F.text == "Запросить проверку")
async def check_schedule(message: Message):
    if message.from_user.id in admins:
        try:
            changes = parse()
            if changes:
                for direction in changes:
                    change = await get_changes_or_create(changes[direction][0], changes[direction][1])
                    if change:
                        for user_id in await get_users_with_agreement(changes[direction][0].split()[-1]):
                            await bot.send_message(int(user_id), f"{change[0]}\n{change[1]}")
                await message.answer("Проверка успешно выполнена")
        except SQLAlchemyError:
            await message.answer("Ошибка при проверке расписания")
    else:
        await message.answer("У вас нет прав доступа для выполнения этой команды")


@router.message()
async def error(message: Message):
    await message.answer("Введена неправильная команда")
