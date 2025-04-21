from MainKeyboard.main_keyboard import create_keyboard
import time

async def my_posts(self, user_id: int):
    async with self.db.pool.acquire() as conn:
        messages_single_posts = await conn.fetch("SELECT message_text FROM vkprod9_posts WHERE user_id = $1",
                                user_id)

        messages_multiply_posts = await conn.fetch("SELECT posts_text FROM vkprod9_multiply_posts WHERE user_id = $1",
                                user_id)

        all_single_posts_messages = [record['message_text'] for record in messages_single_posts]
        all_multiply_posts_messages = [record['posts_text'] for record in messages_multiply_posts]

    result_single_posts = (', '.join(all_single_posts_messages))
    result_multiply_posts = (', '.join(all_multiply_posts_messages))

    try:
        await self.send_message(
            user_id,
            f"Все посты, введенные вами.\nПосты, отправленные индивидуально: {result_single_posts}\nПосты, отправленные используя функцию подборки: {result_multiply_posts}",
            self.create_keyboard(self)
        )
    except Exception as e:
        print(f"Ошибка в handle_start: {e}")
        await self.send_message(user_id, "⚠ Произошла ошибка при запуске")