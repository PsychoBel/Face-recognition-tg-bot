import logging
import gc
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook
from my_bot.model import FullModel, transform
import os
import cv2



# Set API_TOKEN. You must have your own.
BOT_TOKEN = os.environ['BOT_TOKEN']

# webhook settings
WEBHOOK_HOST = os.environ['WEBHOOK_HOST_ADDR']
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.environ['PORT']
# Configure logging.
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher.
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

buttons_for_start = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons_for_start.add(types.KeyboardButton(text="What can you do? \U0001F9D0"))
buttons_for_start.add(types.KeyboardButton(text="Tell me about your creator \U0001F468\U0000200D\U0001F4BB"))
#buttons_for_start.add(types.KeyboardButton(text="What is the weather now? \U00002600"))


@dp.message_handler(commands=['start'], state='*')
async def satrt(message: types.Message):
    """Test function."""
    global user_name
    user_name = str(message.from_user.first_name)
    await message.answer(text=f"Hi, *{user_name}*, \nI am very smart bot \U0001F913, what can I do for you?",
                         reply_markup=buttons_for_start, parse_mode='Markdown')


@dp.message_handler(lambda message: message.text == "Tell me about your creator \U0001F468\U0000200D\U0001F4BB",
                    state='*')
@dp.message_handler(commands=['creator'], state='*')
async def creator(message: types.Message):
    """Displays information about the bot's Creator."""

    await message.answer(text="He is student of Data Analytics School (by X5 Retail Group). Work in PwC (Data analyst)"
    " and in 'School of programmers' (Teacher)\n\nLink to GitHub \U0001F4BB: https://github.com/PsychoBel\nContact with him \U0001F4EB: @psycho1388", reply_markup=buttons_for_start)


@dp.message_handler(lambda message: message.text == "What can you do? \U0001F9D0", state='*')
@dp.message_handler(commands=['help'], state='*')
async def help_message(message: types.Message):
    """
    Outputs a small instruction when the corresponding command is received.
    """

    await message.answer(text="This bot can find faces in photos and determine gender \U0001F46B\n"
                              "All you have to do is *send me a photo showing the face*", parse_mode='Markdown')


@dp.message_handler(content_types=['photo'])
async def predict(message):
    """Function for image transformation."""
    global user_id
    user_id = str(message.from_user.id)
    in_path = 'input_photo' + user_id + '.jpg'
    out_path= 'output_photo' + user_id + '.jpg'


    model = FullModel()

    await message.photo[-1].download(in_path)
    await message.answer(text='Nice \U0001F60D')

    img = cv2.imread(os.path.join(in_path))
    boxes, genders, ages = model.predict(img)
    img_c = transform(img, boxes, genders, ages)
    cv2.imwrite(os.path.join(out_path), img_c)
    with open(out_path, 'rb') as file:
        await message.answer_photo(file, caption='I find you \U0001F92A')

    del img
    os.remove(in_path)
    os.remove(out_path)
    gc.collect()

    @dp.message_handler(state='*')
    async def catch_bad_commands(message: types.Message):
        await message.answer(text="Sorry, I don't know this command \U0001F62C\n"
                                  "Write *'/'* to see list of commands or press */help*",
                             reply_markup=buttons_for_start, parse_mode='Markdown')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Start webhook..\tWEBAPP_HOST-{WEBAPP_HOST}; WEBAPP_PORT-{WEBAPP_PORT};\n"
                 f"WEBAPP_URL-{WEBHOOK_URL};")


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')
