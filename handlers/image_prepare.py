import random
import time

from aiogram import types,Router,F,Bot
from aiogram.filters.command import Command
from typing import List
from aiogram.filters.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from glob import glob
from aiogram.utils.media_group import MediaGroupBuilder
import cv2
import os
import shutil

from keyboards import get_next_btn
class Get_images(StatesGroup):
    waiting_images = State()
router = Router()

@router.message(Command("start"))
async def cmd_start(message:types.Message,state: FSMContext):
    # await state.set_state(User.waiting_name.state)
    images = glob("./statics/main/*.jpg")
    if not images:
        await message.answer("Пока у нас нет фильтров")

    for image_path in images:
        image = types.FSInputFile(image_path)
        image_splited = image_path.split("/")[-1].split("\\")[-1].split(".")
        image_name = image_splited[1]
        image_callback = image_splited[0]
        await state.update_data({"event":image_callback})
        next_btn = await get_next_btn("Перейти","send_files")
        await message.answer_photo(photo=image,caption=image_name,reply_markup=next_btn)

@router.callback_query(F.data == "send_files")
async def send_photo(call: types.CallbackQuery,state: FSMContext):
    await state.set_state(Get_images.waiting_images.state)
    await call.answer(text=f"Загрузите фотографии (группой или одно) ")

@router.message(Get_images.waiting_images)
async def photo_prepare(message: types.Message,state: FSMContext,bot:Bot):
    try:
        album = message.photo[-1]
        print(album)
        if not os.path.isdir(f"before_prepare_images"):
            os.mkdir(f"before_prepare_images")
        if not os.path.isdir(f"before_prepare_images/{message.from_user.id}"):

            os.mkdir(f"before_prepare_images/{message.from_user.id}")

        # print(obj.file_id)
        await bot.download(
                    album.file_id,
                    destination=f'before_prepare_images/{message.from_user.id}/{album.file_id}.jpg'
                )
        photos = glob(f"./before_prepare_images/{message.from_user.id}/*.jpg")

        album_builder = MediaGroupBuilder(
            caption="Преобразованные изображения"
        )
        data = await state.get_data()

        if "event" not in data:
            await message.answer(text=f"Повторите вход через /start")
            shutil.rmtree(f"before_prepare_images/{message.from_user.id}")
            return
        for photo in photos:
            #главная обработка как тебе нужно
            file = None
            if data["event"] == "grayscale":
                file = cv2.imread(photo[2:], cv2.IMREAD_GRAYSCALE)

            try:
                album_builder.add(
                    type="photo",
                    media=types.BufferedInputFile(bytearray(file),filename=f"{random.randint(1000,10000000)}.jpg")
                )
            except PermissionError:
                print("PermissionError: The file is being used by another process. Waiting for 5 seconds...")
                time.sleep(5)
        await message.answer_media_group(
            # Не забудьте вызвать build()
            media=album_builder.build()
        )
        shutil.rmtree(f"before_prepare_images/{message.from_user.id}")
    except Exception as e:
        print(e)
        shutil.rmtree(f"before_prepare_images/{message.from_user.id}")





#
#
# @router.message(User.waiting_name,F.text)
# async def waiting_name(message: types.Message, state: FSMContext):
#     if "1" in message.text:
#         await message.answer("Ошибка ввода 1 не должно быть")
#         return
#
#     await state.update_data(name=message.text) # a['name'] = message.text
#     await state.set_state(User.waiting_surname.state)
#
#     await message.answer(f"Ура ваше имя <b>{message.text}</b> введите фамилию",
#                          parse_mode="HTML")
#
# @router.message(User.waiting_surname,F.text)
# async def waiting_surname(message: types.Message, state: FSMContext):
#     if "1" in message.text:
#         await message.answer("Ошибка ввода 1 не должно быть")
#         return
#
#     await state.update_data(surname=message.text)
#     await state.set_state(User.waiting_photo.state)
#     data = await state.get_data()
#
#     await message.answer(f"Ура ваше имя <b>{data['name']}</b> \n Ура ваша фамилия {data['surname']}",
#                          parse_mode="HTML")
#
# @router.callback_query(F.data == "Груша")
# async def names_prepare(call: types.CallbackQuery):
#     await call.answer(text=f"Вы нажали на {call.data}",show_allert = True)
# @router.message(User.waiting_photo,F.photo)
# async def waiting_name(message: types.Message, state: FSMContext):
#
#
#     await state.set_state(None)
#     await state.clear()
#     await message.answer(f"Ура фото тут",
#                          parse_mode="HTML")
#
#
#
#



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


