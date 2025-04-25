import time
import asyncpg


async def my_posts(self, user_id):
    current_timestamp = int(time.time())
    async with self.db.pool.acquire() as conn:
        query = """
            SELECT 
                p.publish_date,
                p.owner_id,
                p.text,
                c.channel_name
            FROM 
                vkprod15_multiply_posts_timestamp p
            LEFT JOIN 
                vkprod11_channels c ON p.owner_id::TEXT = c.owner_id
            WHERE 
                p.publish_date > $1
                AND p.user_id = $2
            ORDER BY 
                p.publish_date ASC;
        """

        try:
            records = await conn.fetch(query, current_timestamp, user_id)

            if not records:
                print("Нет запланированных постов.")
                return await self.send_message(
                    user_id,
                    "У вас нет запланированных постов.",
                    keyboard=self.create_keyboard(self)
                )

            print("Запланированные посты:")
            print("-" * 50)
            for record in records:
                publish_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(record["publish_date"]))

                response = (
                    f"Дата: {publish_time}\n"
                    f"Канал: {record['owner_id']}\n"
                    f"Название: {record['channel_name'] or 'Не указано'}\n"
                    f"Текст: {record['text'][:50]}..."
                )

                print(response)
                # Если нужно отправить пользователю:
                await self.send_message(
                    user_id,
                    response,
                    keyboard=self.create_keyboard(self)
                )

        except Exception as e:
            print(f"Ошибка при получении постов: {e}")
            await self.send_message(
                user_id,
                "Произошла ошибка при получении постов.",
                keyboard=self.create_keyboard(self)
            )