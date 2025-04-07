async def process_existed_channel_club_input(self, user_id: int, text: str, api_key: str, state_data: dict):
    """Обработка id канала"""

    if len(text) == 9 and text.isdigit():

        try:
            # Сохраняем в базу данных
            await self.db.save_existed_channel_club(
                user_id=user_id,
                club_id=text,
                api_key=api_key,
                session_id=state_data["session_id"],
            )

            self.awaiting_input[user_id] = {
                "state": "awaiting_channel_name",
                "club_id": text,
                "session_id": state_data["session_id"],
            }

            await self.send_message(
                user_id,
                f"ID группы {text} успешно сохранено. Введите название канала: ",
                keyboard=self.create_publish_time_keyboard(self)
            )

        except Exception as e:
            await self.send_message(
                user_id,
                f"❌ Ошибка при сохранении ключа: {str(e)}",
                self.create_keyboard(self)
            )

    else:
        await self.send_message(
            user_id,
            f"Неверно введеный club_id, введите заново."
        )