import time

async def clear_expired_states(self, timeout: int = 300):
    """Очистка неактивных состояний старше timeout секунд"""
    current_time = time.time()
    expired_users = [
        user_id for user_id, state in self.awaiting_input.items()
        if current_time - state["timestamp"] > timeout
    ]

    for user_id in expired_users:
        try:
            await self.send_message(
                user_id,
                "⏳ Время ожидания истекло. Пожалуйста, начните заново.",
                self.create_keyboard()
            )
            del self.awaiting_input[user_id]
        except Exception as e:
            print(f"Ошибка при очистке состояния для {user_id}: {e}")