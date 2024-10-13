from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="😭 Высшее профессиональное (ВО)")],
        [KeyboardButton(text="🥲 Среднее профессиональное (СПО)")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def change_kb_with_disable(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="❌ Отменить рассылку")],
        [KeyboardButton(text="↩️ Изменить направление")],
        [KeyboardButton(text="💌 Обратная связь")],
        [KeyboardButton(text="🔄 Получить последние изменения")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=False)
    return keyboard

def change_kb_with_enable(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="✅ Включить рассылку")],
        [KeyboardButton(text="↩️ Изменить направление")],
        [KeyboardButton(text="💌 Обратная связь")],
        [KeyboardButton(text="🔄 Получить последние изменения")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=False)
    return keyboard