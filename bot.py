import os
import random
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

TG_SEX_POSES_PATH = 'TgSexPoses'
TG_KUNI_POSES_PATH = 'TgKunePoses'
TG_CUBE_PATH = 'TgCube'

def get_random_photo(folder_path):
    """Возвращает путь к случайному файлу из указанной папки."""
    files = os.listdir(folder_path)
    random_file = random.choice(files)
    return os.path.join(folder_path, random_file)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Покажи что умеешь!", callback_data="secondM"))
    await bot.send_message(message.from_user.id, "Ну что,начнем игру?😏", reply_markup=keyboard, parse_mode="Markdown")
async def send_photo_with_keyboard(chat_id, photo_path, callback_data):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Еще", callback_data=callback_data))
    keyboard.add(types.InlineKeyboardButton(text="В начало", callback_data="secondM"))
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(chat_id, photo, reply_markup=keyboard)

@dp.callback_query_handler(text="secondM")
async def SecondM_command(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Позы для секса", callback_data="send_sex_pose"))
    keyboard.add(types.InlineKeyboardButton(text="Позы для куни", callback_data="send_kuni_pose"))
    keyboard.add(types.InlineKeyboardButton(text="Кубики рандома", callback_data="send_cube"))
    await  call.message.answer("Выбери что хочешь!", reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == 'send_sex_pose')
async def process_callback_sex_pose(callback_query: types.CallbackQuery):
    photo_path = get_random_photo(TG_SEX_POSES_PATH)
    await send_photo_with_keyboard(callback_query.from_user.id, photo_path, 'send_sex_pose')

@dp.callback_query_handler(lambda c: c.data == 'send_kuni_pose')
async def process_callback_kuni_pose(callback_query: types.CallbackQuery):
    photo_path = get_random_photo(TG_KUNI_POSES_PATH)
    await send_photo_with_keyboard(callback_query.from_user.id, photo_path, 'send_kuni_pose')

@dp.callback_query_handler(lambda c: c.data == 'send_cube')
async def process_callback_cube_pose(callback_query: types.CallbackQuery):
    photo_path = get_random_photo(TG_CUBE_PATH)
    await send_photo_with_keyboard(callback_query.from_user.id, photo_path, 'send_cube')

@dp.callback_query_handler(lambda c: c.data == 'start')
async def process_callback_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text="Здарова, пиздолиз!")
    await process_start_command(callback_query.message)

if __name__ == '__main__':
    executor.start_polling(dp)