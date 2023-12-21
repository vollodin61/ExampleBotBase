from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio.client import Redis

bot_token = '6859353795:AAEFQc843Im8E8Ui_irejoolfrL3gIhInmo'
# red = Redis(host='rediska')  # ВЫБЕРИ для докера или локально РЕДИСКУ
red = Redis(host='localhost')
red_storage = RedisStorage(red)
storage = MemoryStorage()
dp = Dispatcher(storage=red_storage)
bot = Bot(token=bot_token, parse_mode="HTML")
