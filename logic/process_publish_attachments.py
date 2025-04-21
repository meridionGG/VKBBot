from datetime import datetime, timezone, timedelta
from Bot.post_to_wall import post_to_wall
from Bot.var import wall_post_access_token
import re

attachments_list = []
links_list = []

async def process_publish_attachments(self, user_id: int, message: str, channel_id: str, state_data: dict, channel_name, attachments):
    session_id = state_data["session_id"]
    # attachments_list = []
    if message == "Да":
        await self.send_message(
            user_id,
            "Можете отправлять фотографии по 1 штуке. По завершении нажмите на кнопку 'Подтвердить' или 'Отменить', чтобы вернуться в главное меню.\nТакже можете только 1 ссылку.",
            keyboard=self.create_multiply_posts_keyboard(self)
        )

    elif attachments != None:
        print('im in process_publish_attachments')
        print(attachments)
        attachments_list.append(attachments)

    elif message != "Подтвердить":
        links_list.append(message)

    elif message == "Подтвердить":
        print(attachments_list)
        await self.loader(self, attachments_list, user_id, session_id)
        attachments_list.clear()
        await self.send_message(
            user_id,
            "Все медиаматериалы успешно загружены. Выберите день публикации.",
            self.create_publish_time_keyboard(self)
        )

        if links_list:
            link = links_list[0]
        else:
            link = None

        self.awaiting_input[user_id] = {
            "state": "awaiting_publish_time_day",
            "session_id": state_data["session_id"],
            "channel_name": channel_name,
            "text": message,
            "link": link,
            "channel_id": channel_id
        }

    if message == "Нет":

        await self.send_message(
            user_id,
            "✅ Пост сохранен без медиаматериалов! Выберите день публикации.",
            keyboard=self.create_publish_time_keyboard(self)
        )

        print(f"Должно вывестить НЕТ {message}")

        self.awaiting_input[user_id] = {
            "state": "awaiting_publish_time_day",
            "session_id": state_data["session_id"],
            "channel_name": channel_name,
            "text": message,
            "link": None,
            "channel_id": channel_id
        }

