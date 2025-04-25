from MainKeyboard.main_keyboard import create_keyboard
import uuid

async def add_channel(self, user_id: int):
    """Обработка команды Новый канал"""

    try:
        if user_id not in self.user_sessions:
            session_id = str(uuid.uuid4())

            self.user_sessions[user_id] = {
                "session_id": session_id,
                "channel_id": None
            }
        else:
            session_id = self.user_sessions[user_id]["session_id"]

        async with self.db.pool.acquire() as conn:
            channel_id = await conn.fetch("SELECT channel_id FROM vkprod11_channels WHERE user_id = $1", #забавно, что message принимает новую переменную
                                           user_id)

            all_channel_ids = [record['channel_id'] for record in channel_id]

        if len(all_channel_ids) > 0:
            result = all_channel_ids[0]

            self.awaiting_input[user_id] = {
                "state": "awaiting_existed_channel_club",
                "api_key": result,
                "session_id": session_id,
            }

            await self.send_message(
                user_id,
                "Вы уже добавили ключ. Введите club_id канала: ",
                keyboard=self.exit_keyboard(self)
            )


        else:

            self.awaiting_input[user_id] = {
                "state": "awaiting_channel",
                "session_id": session_id,
            }

            await self.send_message(
                user_id,
                "Здесь ты можешь добавить свой канал. Необходимо перейти по https://vkhost.github.io/ и нажать на 'VK Admin'. После чего введите ссылку из адресной строки сюда.",
                keyboard=self.exit_keyboard(self)
            )

    except Exception as e:
        print(f"Ошибка в handle_start: {e}")
        await self.send_message(user_id, "⚠ Произошла ошибка при запуске")