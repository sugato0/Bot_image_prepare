import io
import random
import time
import numpy as np
from aiogram import types,Router,F,Bot
from aiogram.filters.command import Command
from typing import List
from aiogram.filters.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from glob import glob
from aiogram.utils.media_group import MediaGroupBuilder
import cv2
from PIL import Image
from keyboards import get_next_btn
router = Router()
media_groups = []
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


        next_btn = await get_next_btn("Перейти",f"send_files_{image_callback}")
        await message.answer_photo(photo=image,caption=image_name,reply_markup=next_btn)

@router.callback_query(F.data.contains("send_files"))
async def send_photo(call: types.CallbackQuery,state: FSMContext):
    image_callback = call.data.split("_")[-1]
    data = await state.get_data()
    if "event" in data:
        await state.update_data({"event": data["event"]+image_callback})
    else:
        await state.update_data({"event": image_callback})
    await call.answer(text=f"Загрузите фотографии (группой или одно) ")


@router.message(F.photo)
async def photo_prepare(message: types.Message,state: FSMContext,bot:Bot):
    try:
        if message.media_group_id in media_groups:
            return
        media_groups.append(message.media_group_id)

        files = message.photo
        file_path = await bot.get_file(files[-1].file_id)
        bin_img = io.BytesIO()
        data = await state.get_data()

        await bot.download_file(
            file_path.file_path,
            bin_img
        )
        buf_file = np.frombuffer(
            bin_img.getvalue(),
            np.uint8
        )
        img = None
        if data["event"] == "grayscale":
            img = cv2.imdecode(buf_file, cv2.IMREAD_GRAYSCALE)
        img = Image.fromarray(img)

        with io.BytesIO() as output:
            img.save(output, format='JPEG')  # You can change the format if needed
            img_bytes = output.getvalue()
        buf_photo = types.BufferedInputFile(
            file=img_bytes,
            filename="new file.jpg"
        )


        await bot.send_photo(
            message.chat.id,
            media=buf_photo
        )
        # await bot.send_photo(
        #     message.chat.id,
        #
        # )


    except Exception as e:
        print(e)

#
#
