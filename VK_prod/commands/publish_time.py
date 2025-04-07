import time
import uuid

async def publish_time(self, user_id: int):
    """Обработка команды 'Один пост -> Сегодня'"""
    if user_id not in self.user_sessions:
        session_id = str(uuid.uuid4())
        self.user_sessions[user_id] = {
            "session_id": session_id,
            "channel_id": None
        }
    else:
        session_id = self.user_sessions[user_id]["session_id"]

    self.awaiting_input[user_id] = {
        "state": "awaiting_publish_time",
        "session_id": session_id,
        "timestamp": time.time()
    }

    await self.send_message(
        user_id,
        "📝 Введите желаемое время отправки поста в виде чч:мм: ",
        keyboard=None
    )