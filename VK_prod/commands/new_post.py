from MainKeyboard.new_post_keyboard import create_new_post_keyboard
import time

async def new_post(self, user_id: int):
    """Обработка команды /start"""
    try:
        keyboard = create_new_post_keyboard(self)
        await self.send_message(
            user_id=user_id,
            text="Привет! Это меню новых постов",
            keyboard=keyboard
        )
    except Exception as e:
        print(f"Ошибка в handle_start: {e}")
        await self.send_message(user_id, "⚠ Произошла ошибка при запуске")