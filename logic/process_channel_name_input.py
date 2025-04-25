async def process_channel_name_input(self, user_id: int, text: str, club_id: str, state_data: dict):
    """Обработка текста канала"""

    try:
        # Сохраняем в базу данных
        await self.db.save_channel_name(
            user_id=user_id,
            channel_name=text,
            club_id=club_id,
            session_id=state_data["session_id"],
        )

        await self.send_message(
            user_id,
            f"Канал {text} успешно сохранен. Можете отправлять посты!",
            keyboard=self.create_keyboard(self)
        )

    except Exception as e:
        await self.send_message(
            user_id,
            f"❌ Ошибка при сохранении ключа: {str(e)}",
            self.create_keyboard(self)
        )
    del self.awaiting_input[user_id]
    del self.user_sessions[user_id]