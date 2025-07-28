import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import FSInputFile, Message, ContentType
from aiogram.enums import ParseMode
from aiogram.filters import Command
from config import BOT_TOKEN
from video_utils import convert_to_circle
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

import asyncio

bot = Bot(
    token=BOT_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "<b>Привет! 👋</b>\n\n"
        "Я — бот, который превращает твое видео в телеграм-кружок 🎥.\n\n"
        "<b>Правила:</b>\n"
        "• Максимальная длительность — <b>60 секунд</b>\n"
        "• Максимальный размер файла — <b>20МБ</b>\n"
        "• Видео должно быть в формате <i>mp4</i>"
    )
    await message.answer(welcome_text)

@dp.message(F.content_type == ContentType.VIDEO)
async def handle_video(message: Message, bot: Bot):
    max_size_bytes = 20 * 1024 * 1024  # 20 MB

    # ✅ Проверка размера ДО скачивания
    if message.video.file_size and message.video.file_size > max_size_bytes:
        await message.answer("⚠️ Видео слишком большое для кружка (максимум 20MB). Отправь файл поменьше.")
        return

    await message.answer("Видео получено. Конвертирую в кружок...")

    # Скачивание файла
    file = await bot.get_file(message.video.file_id)
    file_path = file.file_path
    downloaded_file = await bot.download_file(file_path)

    input_file_path = f"temp_{message.from_user.id}.mp4"
    with open(input_file_path, "wb") as f:
        f.write(downloaded_file.read())

    # Конвертация
    output_file_path = convert_to_circle(input_file_path)

    # Отправка кружка
    video_note = FSInputFile(output_file_path)
    await message.answer_video_note(video_note)

    # Очистка временных файлов
    os.remove(input_file_path)
    os.remove(output_file_path)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())