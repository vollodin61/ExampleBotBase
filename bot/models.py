from datetime import datetime
from typing import Optional

from sqlalchemy import (BigInteger, Integer, String, Column, DateTime, ForeignKey,
						Text, Boolean, MetaData, func, UniqueConstraint)
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from bot.db_cfg import Base

# matadata_obj = MetaData()


class User(Base):
	__tablename__ = "user"
	tg_id: Mapped[int] = mapped_column(unique=True)
	username: Mapped[str] = mapped_column(nullable=True)
	# status: Mapped[str] = mapped_column(nullable=True)
	# first_name: Mapped[str] = mapped_column(nullable=True)
	# last_name: Mapped[str] = mapped_column(nullable=True)

	courses: Mapped[list["Course"]] = relationship(back_populates="users", secondary="courses_users")


class Course(Base):
	__tablename__ = 'course'
	name: Mapped[str] = mapped_column(unique=True)
	# user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
	users: Mapped[list["User"]] = relationship(back_populates="courses", secondary="courses_users")
	short_description: Mapped[str] = mapped_column(nullable=True)


class UserCourse(Base):
	__tablename__ = 'courses_users'  # TODO проверить эту таблицу
	id: Mapped[int] = mapped_column(primary_key=True)
	user_tg_id: Mapped[int] = mapped_column(ForeignKey('user.tg_id', ondelete='CASCADE'), nullable=False)
	course_name: Mapped[str] = mapped_column(ForeignKey('course.name', ondelete='CASCADE'), nullable=False)
	UniqueConstraint('course_id', 'user_id', name='idx_courses_users')
# user_tg_id: Mapped[int] = mapped_column(ForeignKey('user.tg_id', ondelete="RESTRICT"), nullable=True)
# user = relationship('User', back_populates='course')  # orders = relationship('Order', back_populates='courses')


#
# class Webinar(Base):  # TODO Сделать модель Вебинара
# 	__tablename__ = 'webinars'
# 	name: Mapped[str] = mapped_column(unique=True)
# 	users: Mapped[list["User"]] = relationship(back_populates="webinars")


# class Otz(Base):  # TODO Сделать модель Отзывов
# 	pass
#
#
# class Survey(Base):  # TODO Сделать модель Опросов
# 	pass
#
#
# class Club(Base):  # TODO Сделать модель Клуба
# 	pass

#
#
# class Video(Base):  # TODO Сделать модель Видео
# 	__tablename__ = 'videos'
# 	name: Mapped[str] = mapped_column(unique=True)
# 	webinar: Mapped[str] = mapped_column(ForeignKey('webinars.name', ondelete='RESTRICT'))

