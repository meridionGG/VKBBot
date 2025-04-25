from MainKeyboard.main_keyboard import create_keyboard
import uuid

async def process_exit(self, user_id: int):
    try:
        await self.send_message(
            user_id,
            f"Действие отменено.",
            keyboard=self.create_keyboard(self)
        )

    except Exception as e:
        await self.send_message(
            user_id,
            f"❌ Ошибка при сохранении ключа: {str(e)}",
            self.create_keyboard(self)
        )