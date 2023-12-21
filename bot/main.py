import asyncio
import logging

from aiogram import Router
from aiogram.types import Message

from bot.requests import AsyncORM
from bot.bot_cfg import dp, bot


router = Router()


@router.message()
async def echo(msg: Message):
	await msg.answer("Bella ciao!")


async def main():
	logging.basicConfig(level=logging.INFO)
	await AsyncORM.drop_create_tables()
	await AsyncORM.create_course(name='Номер 1')
	await AsyncORM.create_course(name='Номер 2')
	await AsyncORM.create_user(tg_id=3, username='Ilya')
	dp.include_router(router)
	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == "__main__":
	# try:
	asyncio.run(main())
	# except Exception as err:
	# 	print(f'Что-то пошло не так, ошибка:\n{err}')
