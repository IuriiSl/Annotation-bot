import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import questions, getting_file
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode 
from aiogram.fsm.storage.memory import MemoryStorage


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_routers(questions.router, getting_file.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
