import psycopg2

from aiogram.types import Message
from sqlalchemy import select

from bot.db_cfg import async_session_factory, Base, async_engine
from bot.models import Course, User


async def drop_database():
	conn = psycopg2.connect(dbname="postgres", user="postgres", password="123456", host="127.0.0.1")
	cursor = conn.cursor()

	conn.autocommit = True
	# команда для удаления базы данных с именем database
	sql = "DROP DATABASE database"

	cursor.execute(sql)
	print("База данных успешно уничтожена")

	cursor.close()
	conn.close()


def sync_create_database():
	conn = psycopg2.connect(dbname="postgres", user="postgres", password="123456", host="127.0.0.1")
	cursor = conn.cursor()

	conn.autocommit = True
	# команда для создания базы данных с именем database
	sql = "CREATE DATABASE database"

	cursor.execute(sql)
	print("База данных успешно создана")

	cursor.close()
	conn.close()


class AsyncORM:
	@staticmethod
	async def drop_models():
		async with async_engine.begin() as conn:
			await conn.run_sync(Base.metadata.drop_all)

	@staticmethod
	async def create_models():
		async with async_engine.begin() as conn:
			await conn.run_sync(Base.metadata.create_all)

	@staticmethod
	async def create_tables():  # TODO здесь нужно убрать дроп, наверное
		async with async_engine.begin() as conn:
			await conn.run_sync(Base.metadata.drop_all)
			await conn.run_sync(Base.metadata.create_all)

	@staticmethod
	async def insert_user_from_bot(msg: Message, course: str = None):
		async with async_session_factory() as sess:
			# if select(User).filter_by(tg_id=msg.from_user.id):
			# 	pass
			# else:
			new_user = User(tg_id=msg.from_user.id,
							username=msg.from_user.username,
							status='active',
							first_name=msg.from_user.first_name,
							last_name=msg.from_user.last_name,
							)

			sess.add(new_user)
			# await sess.flush() не нужна тут, но пусть глаза мозолит, чтоб запомнить, что такая есть
			await sess.commit()

	@staticmethod
	async def create_user(tg_id: int, username: str = None):
		async with async_session_factory() as sess:
			# if select(User).filter_by(tg_id=msg.from_user.id):
			# 	pass
			# else:
			new_user = User(tg_id=tg_id, username=username)

			sess.add(new_user)
			# await sess.flush() не нужна тут, но пусть глаза мозолит, чтоб запомнить, что такая есть
			await sess.commit()

	@staticmethod
	async def create_course(name: str, short_description: str = None):
		async with async_session_factory() as sess:
			sess.add(Course(name=name, short_description=short_description))
			# await sess.flush() не нужна тут, но пусть глаза мозолит, чтоб запомнить, что такая есть
			await sess.commit()

	@staticmethod
	async def insert_course_to_user(course: str, tg_id: str):
		async with async_session_factory() as sess:

			stmt = select(User).where(User.tg_id == tg_id)
			user: User | None = await sess.scalar(stmt)
			c_stmt = select(Course).filter_by(name=course)
			course: Course | None = await sess.scalar(c_stmt)
			# await user.courses.append("Сарафанка")  # TODO: тут подследние попытки научиться добавлять курс к пользователю
			print(f"{'*' * 88}\n{user = }\n{course = }\n{'*' * 88}")
			return user


