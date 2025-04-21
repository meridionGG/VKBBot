from MainKeyboard.main_keyboard import create_keyboard
import uuid

async def handle_timezone(self, user_id: int):
    """Обработка команды Новый канал"""
    try:

        await self.send_message(
            user_id,
            "Укажите ваш часовой пояс от -12 до +14: ",
            keyboard=None
        )

        if user_id not in self.user_sessions:
            session_id = str(uuid.uuid4())

        else:
            session_id = self.user_sessions[user_id]["session_id"]

        self.awaiting_input[user_id] = {
            "state": "awaiting_timezone",
            "session_id": session_id,
        }

    except Exception as e:
        print(f"Ошибка в handle_start: {e}")
        await self.send_message(user_id, "⚠ Произошла ошибка при запуске")