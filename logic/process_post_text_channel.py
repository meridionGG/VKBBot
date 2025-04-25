from datetime import datetime

async def process_post_text_channel(self, user_id: int, text: str, state_data: dict):
    """Обработка текста Канала"""
    print(text)
    async with self.db.pool.acquire() as conn:
        channel_names = await conn.fetch("SELECT channel_name FROM vkprod11_channels WHERE user_id = $1",
                                       user_id)

        all_channel_names = [record['channel_name'] for record in channel_names]

    if text in all_channel_names:
        self.awaiting_input[user_id] = {
            "state": "awaiting_post_text",
            "channel_name": text,
            "session_id": state_data["session_id"]
        }

        await self.send_message(
            user_id,
            f"Канал успешно выбран! Выберите текст поста: ",
        )


    else:
        await self.send_message(
        user_id,
        f"Действие отменено.",
        self.create_keyboard(self)
        )

        del self.awaiting_input[user_id]