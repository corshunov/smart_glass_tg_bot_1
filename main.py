import asyncio
from os import getenv
from pathlib import Path
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

video_fext = "mp4"

controller_dpath = Path.home() / "smart_glass" / "controller"
controller_data_dpath = controller_dpath / "data"
controller_videos_dpath = controller_data_dpath / "videos"
controller_requests_dpath = controller_data_dpath / "requests"

update_ref_fpath = controller_requests_dpath / "update_ref"
record_fpath = controller_requests_dpath / "record"

recording_video_fpath = controller_videos_dpath / "recording.{video_fext}"

manual_mode_fpath = controller_data_dpath / "manual_mode"
glass_state_on_fpath = controller_data_dpath / "glass_state_on"

if len(sys.argv) == 2 and sys.argv[1] == "--dev":
    CHAT_ID = getenv("CHAT_ID_DEV")
else:
    CHAT_ID = getenv("CHAT_ID")

TOKEN = getenv("CONTROLLER_BOT_TOKEN")
ADMIN_ID = getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

bot_cmds = [
    'start',
    'help',

    'manualOn',
    'manualOff',

    'glassOn',
    'glassOff',

    'showFrameAndCoords',

    'showRef',
    'updateRef',

    'showCoords',
    'updateCoords',

    'recordVideo',
]

def is_private_user(msg):
    if msg.chat.id == msg.from_user.id:
        return True
    
    return False

def is_admin(msg):
    print(msg.from_user.id, type(msg.from_user.id))
    if msg.from_user.id == ADMIN_ID:
        return True
    
    return False

@dp.message(Command('start'))
async def start_command(message: Message):
    if not is_private_user(message):
        return

    await message.answer("Welcome! Use /help to see details about bot.")

@dp.message(Command('help'))
async def help_command(message: Message):
    if not is_private_user(message):
        return

    cmd_list = "\n".join([f"/{cmd}" for cmd in bot_cmds])
    await message.answer(f"I am Smart Glass Controller Bot.\n\nI provide control interface to smart glass.\n\nAvailable commands:\n{cmd_list}")

@dp.message(Command('manualOn'))
async def update_command(message: Message):
    if not is_private_user(message):
        return

    if not is_admin(message):
        return

    if manual_mode_fpath.is_file():
        await bot.answer("MANUAL mode is already enabled!")
        return

    manual_mode_fpath.touch()
    
@dp.message(Command('manualOff'))
async def update_command(message: Message):
    if not is_private_user(message):
        return

    if not is_admin(message):
        return

    if not manual_mode_fpath.is_file():
        await bot.answer("MANUAL mode is already disabled!")
        return

    manual_mode_fpath.unlink()

@dp.message(Command('glassOn'))
async def update_command(message: Message):
    if not is_private_user(message):
        return

    if not manual_mode_fpath.is_file():
        await bot.answer("MANUAL mode is disabled!")
        return

    if manual_state_on_fpath.is_file():
        await bot.answer("Glass is already ON")
        return

    manual_state_on_fpath.touch()
    
@dp.message(Command('glassOff'))
async def update_command(message: Message):
    if not is_private_user(message):
        return

    if not manual_mode_fpath.is_file():
        await bot.answer("MANUAL mode is disabled!")
        return

    if not manual_state_on_fpath.is_file():
        await bot.answer("Glass is already OFF")
        return

    manual_state_on_fpath.unlink()

@dp.message(Command('showFrameAndCoords'))
async def update_command(message: Message):
    if not is_private_user(message):
        return

@dp.message(Command('showRefAndCoords'))
async def update_command(message: Message):
    if not is_private_user(message):
        return

@dp.message(Command('updateRef'))
async def update_command(message: Message):
    if not is_private_user(message):
        return

    update_ref_fpath.touch()
    await bot.send_message(CHAT_ID, f"UPDATE request\nUser: @{message.from_user.username}")

@dp.message(Command('updateCoords'))
async def update_command(message: Message):
    if not is_private_user(message):
        return

@dp.message(Command('recordVideo'))
async def record_command(message: Message):
    if not is_private_user(message):
        return
    
    if recording_video_fpath.is_file():
        await bot.answer("Video is already recording")
        return

    record_fpath.touch()
    await bot.send_message(CHAT_ID, f"RECORD request\nUser: @{message.from_user.username}")

#@dp.message()
#async def any_command(message: Message):
    #await message.answer("Answered by Controller")

async def main():
    await bot.send_message(CHAT_ID, "Controller Bot started.")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
