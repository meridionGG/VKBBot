async def process_timezone(self, user_id: int, timezone: str, state_data: dict):
    if -12 <= int(timezone) <= 14:
        try:
            # Сохраняем в базу данных
            await self.db.save_timezone(
                user_id=user_id,
                timezone=timezone,
                session_id=state_data["session_id"],
            )

            await self.send_message(
                user_id,
                f"Ваше время {timezone} успешно сохранено.",
                keyboard=self.create_keyboard(self)
            )

        except Exception as e:
            await self.send_message(
                user_id,
                f"❌ Ошибка при сохранении ключа: {str(e)}",
                self.create_keyboard(self)
            )

        del self.awaiting_input[user_id]

    else:
        await self.send_message(
            user_id,
            f"Неккоректный ввод. Укажите ваш часовой пояс от -12 до +14: ",
            keyboard=None
        )