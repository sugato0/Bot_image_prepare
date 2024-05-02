from aiogram import types,Router,F,Bot
from aiogram.filters.command import Command
from aiogram.filters.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

import cv2

class User(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_photo = State()
router = Router()

@router.message(Command("start"))
async def cmd_start(message:types.Message,state: FSMContext):
    # await state.set_state(User.waiting_name.state)
    names = ["Груша","Яблоко","Слива"]
    a = [[types.KeyboardButton(text=i)] for i in names]
    keyboard = types.ReplyKeyboardMarkup(keyboard=a)

    b = [[types.InlineKeyboardButton(text=i,callback_data=str(i))] for i in names]
    keyboard_2 = types.InlineKeyboardMarkup(inline_keyboard=b)

    await message.answer(text = "Выберите еду",reply_markup=keyboard)
    await message.answer(text="Выберите еду - 2", reply_markup=keyboard_2)



@router.message(User.waiting_name,F.text)
async def waiting_name(message: types.Message, state: FSMContext):
    if "1" in message.text:
        await message.answer("Ошибка ввода 1 не должно быть")
        return

    await state.update_data(name=message.text) # a['name'] = message.text
    await state.set_state(User.waiting_surname.state)

    await message.answer(f"Ура ваше имя <b>{message.text}</b> введите фамилию",
                         parse_mode="HTML")

@router.message(User.waiting_surname,F.text)
async def waiting_surname(message: types.Message, state: FSMContext):
    if "1" in message.text:
        await message.answer("Ошибка ввода 1 не должно быть")
        return

    await state.update_data(surname=message.text)
    await state.set_state(User.waiting_photo.state)
    data = await state.get_data()

    await message.answer(f"Ура ваше имя <b>{data['name']}</b> \n Ура ваша фамилия {data['surname']}",
                         parse_mode="HTML")

# @router.callback_query(F.data == "Груша")
# async def names_prepare(call: types.CallbackQuery):
#     await call.answer(text=f"Вы нажали на {call.data}",show_allert = True)
# @router.message(User.waiting_photo,F.photo)
# async def waiting_name(message: types.Message, state: FSMContext):


#     await state.set_state(None)
#     await state.clear()
#     await message.answer(f"Ура фото тут",
#                          parse_mode="HTML")







# @router.message(F.photo)
# async def download_photo(message: types.Message,bot: Bot):
#
#
#     await bot.download(
#         message.photo[-1],
#         destination=f'saved_images/{message.photo[-1].file_id}.jpg'
#     )
#     path = f"saved_images/{message.photo[-1].file_id}.jpg"
#     file = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
#     cv2.imwrite(f"new_{message.photo[-1].file_id}.jpg",file)
#     path1 = f"new_{message.photo[-1].file_id}.jpg"
#     image = types.FSInputFile(path1)
#
#     await message.answer_photo(photo=image,
#                                caption="Вот изображение забирай обратно")


