from datetime import datetime


async def process_publish_time_day(self, user_id: int, message: str, text: str, channel_id: str, channel_name, state_data: dict, link):

    print(state_data)

    time = int(datetime.now().timestamp())
    print(message)
    text_day = message

    try:
        #Переходим к выбору времени публикации
        self.awaiting_input[user_id] = {
            "state": "awaiting_publish_time_time",
            "session_id": state_data["session_id"],
            "channel_id": channel_id,
            "channel_name": channel_name,
            "text": text,
            "link": link,
            "publish_day": text_day,
            "timestamp": time
        }

        await self.send_message(
            user_id,
            f"✅ Пост сохранен! Выберите время публикации в виде чч:мм. Учитывайте, что посты будут выкладываться по Московскому времени: ",
        )

    except Exception as e:
        await self.send_message(
            user_id,
            f"❌ Ошибка при сохранении поста: {str(e)}",
            self.create_keyboard(self)
        )