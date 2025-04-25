import time
import uuid

async def multiply_posts(self, user_id: int):
    #должна быть проверка на доступные каналы
    async with self.db.pool.acquire() as conn:
        channel_ids = await conn.fetch("SELECT channel_name FROM vkprod11_channels WHERE user_id = $1",
                                       user_id)

        all_channel_ids = [record['channel_name'] for record in channel_ids]
        print(f"These {all_channel_ids}")
        result = ", ".join(all_channel_ids)

    if str(channel_ids) == '[]':
        await self.send_message(
            user_id,
            "У вас нет доступных каналов. Добавьте используя 'Мои каналы'.",
            keyboard=self.create_keyboard(self)
        )

    else:
        if user_id not in self.user_sessions:
            session_id = str(uuid.uuid4())
            print(session_id)

            self.user_sessions[user_id] = {
                "session_id": session_id,
                "channel_id": None
            }

        else:
            session_id = self.user_sessions[user_id]["session_id"]

        self.awaiting_input[user_id] = {
            "state": "awaiting_multiply_posts_text",
            "session_id": session_id,
        }

        await self.send_message(
            user_id,
            "Можете ввести текст поста.",
            keyboard=self.exit_keyboard(self)
        )