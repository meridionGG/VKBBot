import asyncpg
import time

async def list_my_channels(self, user_id: int):
    """Обработка команды Список каналов"""
    async with self.db.pool.acquire() as conn:
        channel_names = await conn.fetch("SELECT channel_name FROM vkprod11_channels WHERE user_id = $1",
                                       user_id)

        #print(channel_ids, type(str(channel_ids)))
        all_channel_ids = [record['channel_name'] for record in channel_names]
        print(all_channel_ids)
        result = ", ".join(all_channel_ids)

    if str(all_channel_ids) =="[]":
        await self.send_message(
            user_id,
            "Вы не добавили пока ни одного канала!"
        )

    try:
        await self.send_message(
            user_id=user_id,
            text=result,
            keyboard=self.create_keyboard(self)
        )
    except Exception as e:
        print(f"Ошибка в handle_start: {e}")
        await self.send_message(user_id, "⚠ Произошла ошибка при запуске")