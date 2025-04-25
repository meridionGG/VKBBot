import json
import asyncio
from cryptography.fernet import Fernet

import aiovk
from aiovk import API, TokenSession
from aiovk.longpoll import BotsLongPoll

from var import chat_access_token, group_id, wall_post_access_token, encryption_key

import time
from MainKeyboard.main_keyboard import create_keyboard
from MainKeyboard.new_post_keyboard import create_new_post_keyboard
from MainKeyboard.new_channels_keyboard import create_my_channels_keyboard
from MainKeyboard.publish_time_keyboard import create_publish_time_keyboard
from MainKeyboard.multiply_posts_keyboard import create_multiply_posts_keyboard
from MainKeyboard.attachments_keyboard import attachments_keyboard
from MainKeyboard.multiply_keyboard import create_multiply_keyboard
from MainKeyboard.done_keyboard import create_done_keyboard
from MainKeyboard.settings_keyboard import create_settings_keyboard
from MainKeyboard.my_posts_keyboard import my_posts_keyboard
from MainKeyboard.exit_keyboard import exit_keyboard
from MainKeyboard.single_post_keyboard import single_post_keyboard

from awaiting_state import handle_awaiting_state
from expired_states import clear_expired_states

from logic.process_post_text import process_post_text
from logic.process_publish_time_day import process_publish_time_day
from logic.process_publish_time_time import process_publish_time_time
from logic.process_channel_input import process_channel_input
from logic.process_channel_name_input import process_channel_name_input
from logic.process_post_text_channel import process_post_text_channel
from logic.process_multiply_posts_text import process_multiply_posts_text
from logic.process_multiply_posts_time import process_multiply_posts_time
from logic.process_channel_club_input import process_channel_club_input
from logic.process_existed_channel_club_input import process_existed_channel_club_input
from logic.process_publish_attachments import process_publish_attachments
from logic.process_multiply_posts_attachments import process_multiply_posts_attachments
from logic.process_multiply_posts_random import process_multiply_posts_random
from logic.process_timezone import process_timezone
from logic.process_exit import process_exit

from commands.start import start
from commands.new_post import new_post
from commands.single_post import single_post
from commands.my_channels import my_channels
from commands.my_posts import my_posts
from commands.settings import settings
from commands.add_channel import add_channel
from commands.list_my_channels import list_my_channels
from commands.multiply_posts import multiply_posts
from commands.handle_mixposts import handle_mixposts
from commands.handle_timezone import handle_timezone

from check_publish_time import check_publish_time

from Multimedia.loader import loader
from Multimedia.correct_attachments import correct_attachments
from Multimedia.multiply_loader import multiply_loader
from Multimedia.multiply_correct_attachments import multiply_correct_attachments

#время
from commands.publish_time import publish_time

from Database.db import Database
from Database.db_config import DB_CONFIG

class VKBot:
    def __init__(self):

        self.f = Fernet(encryption_key) #for encrypted data

        self.db = Database()
        self.session = None
        self.api = None
        self.longpoll = None

        self.wall_session = TokenSession(wall_post_access_token)
        self.wall_api = API(self.wall_session)

        self.create_keyboard = create_keyboard
        self.create_new_post_keyboard = create_new_post_keyboard
        self.create_my_channels_keyboard = create_my_channels_keyboard
        self.create_publish_time_keyboard = create_publish_time_keyboard
        self.create_multiply_posts_keyboard = create_multiply_posts_keyboard
        self.attachments_keyboard = attachments_keyboard
        self.create_multiply_keyboard = create_multiply_keyboard
        self.create_done_keyboard = create_done_keyboard
        self.create_settings_keyboard = create_settings_keyboard
        self.my_posts_keyboard = my_posts_keyboard
        self.exit_keyboard = exit_keyboard
        self.single_post_keyboard = single_post_keyboard

        #Состояния
        self.handle_awaiting_state = handle_awaiting_state
        self.clear_expired_states = clear_expired_states

        #для функционала команд
        self.handle_start = start
        self.handle_new_post = new_post
        self.handle_single_post = single_post
        self.handle_my_channels = my_channels
        self.handle_my_posts = my_posts
        self.handle_settings = settings
        self.handle_add_channel = add_channel
        self.handle_list_my_channels = list_my_channels
        self.handle_mixposts = handle_mixposts
        self.handle_timezone = handle_timezone

        #обработка команд
        self.process_post_text = process_post_text
        self.process_publish_time_day = process_publish_time_day
        self.process_publish_time_time = process_publish_time_time
        self.process_channel_input = process_channel_input
        self.process_channel_name_input = process_channel_name_input
        self.process_post_text_channel = process_post_text_channel
        self.handle_multiply_posts = multiply_posts
        self.process_multiply_posts_text = process_multiply_posts_text
        self.process_multiply_posts_time = process_multiply_posts_time
        self.process_channel_club_input = process_channel_club_input
        self.process_existed_channel_club_input = process_existed_channel_club_input
        self.process_publish_attachments = process_publish_attachments
        self.process_multiply_posts_attachments = process_multiply_posts_attachments
        self.process_multiply_posts_random = process_multiply_posts_random
        self.process_timezone = process_timezone
        self.process_exit = process_exit

        self.check_publish_time = check_publish_time
        self.correct_attachments = correct_attachments
        self.multiply_correct_attachments = multiply_correct_attachments

        self.loader = loader
        self.multiply_loader = multiply_loader

        self.awaiting_input = {}
        self.user_sessions = {}
        self.active_sessions = {}

    async def init_db(self):
        """Инициализация подключения к БД"""
        await self.db.connect(**DB_CONFIG)

    async def send_message(self, user_id: int, text: str, keyboard=None):
        """Улучшенная отправка сообщений"""
        params = {
            'user_id': user_id,
            'message': text,
            'random_id': int(time.time() * 1000),
        }
        if keyboard:
            params['keyboard'] = keyboard
        try:
            await self.api.messages.send(**params)
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")

    async def update_token(self, new_token: str):
        """Безопасное обновление токена"""
        print("Я в update_token")
        print(new_token)

        try:
            self.wall_session = TokenSession(new_token)
            self.wall_api = API(self.wall_session)

        except Exception as e:
            # В случае ошибки возвращаем старый токен
            raise Exception(f"Не удалось обновить токен: {e}. Восстановлен предыдущий токен")

    async def delete_post_wall(self, owner_id: int, post_id: int, keyboard=None):

        params = {
            'owner_id': -owner_id,
            'post_id': post_id,
        }
        print("Я в delete_post_wall")

        try:
            response = await self.wall_api.wall.delete(**params)
            print(response)
        except Exception as e:
            print("Error:", e)
        return True

    async def post_to_wall(self, user_id: int, text: str, publish_date: int, owner_id: int, attachments: str, keyboard=None):
        # Initialize the session with your access token

        # wall_session = aiovk.TokenSession(channel_id)
        # wall_api = aiovk.API(wall_session)

        # owner_id = -int(user_id)
        # print(type(publish_date))
        # Parameters for the post
        params = {
            'owner_id': -owner_id,
            'from_group': 0,
            'message': text,
            'publish_date': publish_date,
            'attachments': f"{attachments}"
        }
        print("Я в main")
        print(attachments)

        try:
            response = await self.wall_api.wall.post(**params)
            print("Post successfully published! Post ID:", response['post_id'])

            await self.db.multiply_posts_post_id_update(
                user_id=user_id,
                owner_id=owner_id,
                text=text,
                post_id=int(response['post_id'])
            )

        except Exception as e:
            print("Error:", e)
        # await self.wall_session.close()
        return True

    async def handle_message(self, user_id: int, text: str, attachments: str):

        print(text)
        message = text
        print(attachments)

        #await self.clear_expired_states(self)

        async with self.db.pool.acquire() as conn:
            time_zone = await conn.fetch("SELECT timezone FROM vkprod10_timezone WHERE user_id = $1",
                                         user_id)

        all_time_zones = [record['timezone'] for record in time_zone]
        if all_time_zones == []:
            time_zone = "+3"  # по стандарту стоит МСК
        else:
            time_zone = all_time_zones[-1]

        # Если есть ожидаемое состояние - обрабатываем его
        if user_id in self.awaiting_input:
            await self.handle_awaiting_state(self, user_id, message, attachments)
            return

        # Обработка основных команд
        command_handlers = {
            'start': self.handle_start,
            'Start': self.handle_start,
            'Старт': self.handle_start,
            'старт': self.handle_start,
            'Новый пост': self.handle_new_post,
            'Один пост': self.handle_single_post,
            'Подборка постов': self.handle_multiply_posts,
            'Мои каналы': self.handle_my_channels,
            'Мои посты': self.handle_my_posts,
            'Настройки': self.handle_settings,
             f"Часовой пояс [GMT {time_zone}]": self.handle_timezone,
            'Перемешать посты': self.handle_mixposts,
            'Добавить канал': self.handle_add_channel,
            'Список каналов': self.handle_list_my_channels,
            'Отмена': self.process_exit
        }

        handler = command_handlers.get(message)

        if handler:
            await handler(self, user_id)
        else:
            await self.send_message(user_id, "Неизвестная команда. Используйте меню.")

    async def run(self):
        """Основной цикл работы бота"""
        await self.init_db()

        self.session = TokenSession(chat_access_token)
        self.api = API(self.session)
        self.longpoll = BotsLongPoll(self.api, group_id, wait=25)

        print("Бот запущен и ожидает сообщений...")
        async for event in self.longpoll.iter():
            if event['type'] == 'message_new':
                msg = event['object']['message']
                print(msg)
                if msg['attachments'] != []:
                    await self.handle_message(msg['from_id'], msg['text'], msg['attachments'][0]['photo']['orig_photo']['url'])
                else:
                    await self.handle_message(msg['from_id'], msg['text'], None)

    async def shutdown(self):
        """Корректное завершение работы"""
        await self.db.close()
        await self.session.close() #возникает ошибка при изменении кода в db.py

async def main():
    bot = VKBot()
    try:
        await bot.run()
    finally:
        await bot.shutdown()

if __name__ == '__main__':
    asyncio.run(main())