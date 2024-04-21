from aiogram.utils.keyboard import InlineKeyboardBuilder

async def get_next_btn(text:str,next_page:str):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=text, callback_data=next_page)
    keyboard.adjust(1)

    return keyboard.as_markup()