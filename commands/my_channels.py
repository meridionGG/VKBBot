from MainKeyboard.new_channels_keyboard import create_my_channels_keyboard
import time

async def my_channels(self, user_id: int):
    """Обработка команды Новый канал"""
    try:
        keyboard = create_my_channels_keyboard(self) #inline
        await self.send_message(
            user_id=user_id,
            text="Выбери из меню нужную опцию: ",
            keyboard=keyboard
        )
    except Exception as e:
        print(f"Ошибка в handle_start: {e}")
        await self.send_message(user_id, "⚠ Произошла ошибка при запуске")