from datetime import datetime

async def process_post_text(self, user_id: int, text: str, channel_name: str, state_data: dict):
    """Обработка текста поста"""
    time = int(datetime.now().timestamp())

    try:
        # Сохраняем в базу данных
        await self.db.save_message_text(
            user_id=user_id,
            text=text, #Текст поста
            channel_name=channel_name, #Имя канала
            session_id=state_data["session_id"],
        )

        # Сохраняем текст для следующего шага
        #self.user_sessions[user_id]["post_text"] = text

        # Переходим к выбору времени публикации
        self.awaiting_input[user_id] = {
            "state": "awaiting_post_attachments",
            "session_id": state_data["session_id"],
            "channel_name": channel_name,
            "text": text,
            "timestamp": time #Могу использовать, но не обязательно
        }

        await self.send_message(
            user_id,
            "✅ Пост сохранен! Будете загружать медиаматериалы?",
            keyboard=self.attachments_keyboard(self)
        )

    except Exception as e:
        await self.send_message(
            user_id,
            f"❌ Ошибка при сохранении поста: {str(e)}",
            self.create_keyboard(self)
        )