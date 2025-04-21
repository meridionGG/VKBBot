from urllib.parse import urlparse, parse_qs

async def process_channel_input(self, user_id: int, text: str, state_data: dict):
    """Обработка текста канала"""

    hash_part = text.split("#")[1]
    params = parse_qs(hash_part)

    vk_apikey = params.get('access_token', [''])[0]

    try:
        # Сохраняем в базу данных
        await self.db.save_channel_id(
            user_id=user_id,
            channel_id=vk_apikey,
            session_id=state_data["session_id"],
        )

        # Сохраняем текст для следующего шага
        #self.user_sessions[user_id]["post_text"] = text

        # Переходим к названию канала
        self.awaiting_input[user_id] = {
            "state": "awaiting_channel_club",
            "session_id": state_data["session_id"],
            "api_key": vk_apikey
        }

        await self.send_message(
            user_id,
            f"Ключ {vk_apikey} успешно сохранен. Введите club_id канала: ",
            keyboard=self.create_publish_time_keyboard(self)
        )

    except Exception as e:
        await self.send_message(
            user_id,
            f"❌ Ошибка при сохранении ключа: {str(e)}",
            self.create_keyboard(self)
        )
    #del self.awaiting_input[user_id]