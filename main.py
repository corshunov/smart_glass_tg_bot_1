import asyncio
from collections import namedtuple
from os import getenv
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

cmd = namedtuple('cmd', ['command', 'description'])

home_dpath = Path.home()
requests_dpath = home_dpath / "smart_glass_controller" / "data" / "requests"
update_ref_fpath = requests_dpath / "update_ref"
record_fpath = requests_dpath / "record"

CHAT_ID = getenv("CHAT_ID")
TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

bot_cmds = [
    cmd(command='/start', description='Start the bot'),
    cmd(command='/help', description='Get help'),
    cmd(command='/updateRef', description='Set new reference frame'),
    cmd(command='/record', description='Record video for 5 seconds'),
]

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.reply("Welcome! Use /help to see available commands.")

@dp.message(Command('help'))
async def help_command(message: Message):
    command_list = "\n".join([f"{cmd.command} - {cmd.description}" for cmd in bot_cmds])
    await message.reply(f"Available commands:\n{command_list}")

@dp.message(Command('updateRef'))
async def updateRef_command(message: Message):
    update_ref_fpath.touch()

@dp.message(Command('record'))
async def cmd_turnOn(message: Message):
    record_fpath.touch()

async def main():
    await bot.send_message(CHAT_ID, f"Smart Glass Controller started.")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
