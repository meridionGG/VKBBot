from datetime import datetime, timezone, timedelta

posts = []

async def process_multiply_posts_text(self, user_id: int, message: str, state_data: dict):
    print(message)

    # await self.send_message(
    #     user_id,
    #     f"Нажмите на кнопку 'Завершить', чтобы перейти к выбору времени или введите текст нового поста.",
    #     self.create_done_keyboard(self)
    # )

    if message == "Завершить":

        await self.send_message(
            user_id,
            f"Посты успешно загружены. Выберите время публикации в формате ЧЧ:ММ, в одном сообщении с новой строки. Вводите время в соответствии с количеством постов, иначе посты могут не опубликоваться.",
            keyboard=None
        )

        self.awaiting_input[user_id] = {
            "state": "awaiting_process_multiply_posts_time", #меняем на выбор времени
            "session_id": state_data["session_id"]
        }

    elif message == "Отмена":
        await self.send_message(
            user_id,
            f"Действие отменено.",
            self.create_keyboard(self)
        )

        del self.awaiting_input[user_id]

    else:
        await self.db.save_posts_text(
            user_id=user_id,
            posts=message,  # vk_api_key
            session_id=state_data["session_id"],
        )

        await self.send_message(
            user_id,
            f"Пост успешно загружен.\nХотите добавить медиаматериалы?",
            self.attachments_keyboard(self)
        )

        self.awaiting_input[user_id] = {
            "state": "awaiting_process_multiply_posts_attachments",
            "user_id": user_id,
            "posts": message,
            "session_id": state_data["session_id"],
        }
