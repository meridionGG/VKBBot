async def process_multiply_posts_random(self, user_id: int, message: str, state_data: dict):
    """Обработка id канала"""

    if message == "Да":

        self.awaiting_input[user_id] = {
            "state": "awaiting_process_multiply_posts_time",
            "answer": message,
            "session_id": state_data["session_id"],
        }

    elif message == "Нет":

        self.awaiting_input[user_id] = {
            "state": "awaiting_process_multiply_posts_time",
            "answer": message,
            "session_id": state_data["session_id"],
        }

    else:
        await self.send_message(
            user_id,
            f"Не понимаю, введите заново."
        )