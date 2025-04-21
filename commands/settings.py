import time

async def settings(self, user_id: int):
    """Обработка команды /start"""
    try:
        await self.send_message(
            user_id=user_id,
            text="Вы перешли в Настройки",
            keyboard=await self.create_settings_keyboard(self, user_id)
        )
    except Exception as e:
        print(f"Ошибка в handle_start: {e}")
        await self.send_message(user_id, "⚠ Произошла ошибка при запуске")

