from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot.keyboards.all_kb import start_kb, change_kb_with_enable, change_kb_with_disable
from data_base.queries import set_user, change_user_direction, disable_agreement, enable_agreement, disable_direction, \
    get_last_changes_query

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await set_user(tg_id=message.from_user.id)

    await message.answer(
        "Привет! Я бот расписания ХИИК.\nВам необходимо выбрать на клавиатуре ступень вашего образования.",
        reply_markup=start_kb(message.from_user.id))


@router.message(F.text.contains("профессиональное"))
async def choose_vo_direction(message: Message):
    await change_user_direction(tg_id=message.from_user.id, direction=message.text[2:])
    await message.answer(
        f"Вы успешно подписались на рассылку изменения расписания {message.text[2:]}.\nВам начнут приходить изменения со следующего дня.\nДля отмены или изменения направления выберите необходимые кнопки на клавиатуре.",
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
    await message.answer("Рассылка была выключена.\nВновь выберите направление, чтобы вернуть рассылку",
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


@router.message()
async def error(message: Message):
    await message.answer("Введена неправильная команда")
