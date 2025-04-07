from datetime import datetime

async def process_post_text_channel(self, user_id: int, text: str, state_data: dict):
    """Обработка текста Канала"""
    print(text)
    async with self.db.pool.acquire() as conn:
        channel_names = await conn.fetch("SELECT channel_name FROM vkprod9_channels WHERE user_id = $1",
                                       user_id)

        channel_ids = await conn.fetch("SELECT channel_id FROM vkprod9_channels WHERE channel_name = $1",
                                       text)

        all_channel_names = [record['channel_name'] for record in channel_names]
        all_channel_ids = [record['channel_id'] for record in channel_ids]

    if text in all_channel_names:
        self.awaiting_input[user_id] = {
            "state": "awaiting_post_text",
            "channel_id": all_channel_ids[0],
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
        f"❌ Ошибка при сохранении поста: ",
        self.create_keyboard(self)
        )