from MainKeyboard.main_keyboard import create_keyboard
import time

async def settings(self, user_id: int):
    """Обработка команды /start"""
    try:
        keyboard = create_keyboard(self)
        await self.send_message(
            user_id=user_id,
            text="Привет! Я бот для управления постами. Вот доступные команды:",
            keyboard=keyboard
        )
    except Exception as e:
        print(f"Ошибка в handle_start: {e}")
        await self.send_message(user_id, "⚠ Произошла ошибка при запуске")