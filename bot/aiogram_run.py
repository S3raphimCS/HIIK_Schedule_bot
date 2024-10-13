import datetime
from multiprocessing import Process

import asyncio
from create_bot import bot, dp, admins
from handlers.start import router
from bot_stop import stop_bot
from data_base.base import create_tables
from data_base.queries import get_changes_or_create, get_users_with_agreement
from utils.changes_request import parse

async def scheduler():
    checking_time = ["12:00",
                     "14:00",
                     "16:00",
                     "17:00",
                     "18:00",
                     "19:00",
                     "20:00",
                     "21:00"]

    while True:
        if datetime.datetime.now().strftime('%H:%M') in checking_time:
            changes = parse()
            if changes:
                for direction in changes:
                    change = await get_changes_or_create(changes[direction][0], changes[direction][1])
                    if change:
                        for user_id in await get_users_with_agreement(changes[direction][0].split()[-1]):
                            await bot.send_message(int(user_id), f"{change[0]}\n{change[1]}")


        await asyncio.sleep(55)


def worker():
    asyncio.run(scheduler())

async def start_bot():
    await create_tables()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f'Я запущен🥳.')
        except:
            pass

async def main():

    # регистрация функций
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Регистрация роутеров
    dp.include_router(router)

    process = Process(target=worker)
    process.start()

    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
