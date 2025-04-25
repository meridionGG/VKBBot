import json
import time

async def my_posts_keyboard(self, user_id):
    """Создание клавиатуры, которая работает во всех клиентах"""

    async with self.db.pool.acquire() as conn:
        # Получаем все каналы пользователя
        channels = await conn.fetch(
            "SELECT channel_id, owner_id FROM vkprod9_channels WHERE user_id = $1",
            user_id
        )

    if not channels:
        print("У пользователя нет каналов.")
        return

    for channel in channels:
        owner_id = channel['owner_id']

        # Получаем будущие посты (ID, текст, время, вложения)
        async with self.db.pool.acquire() as conn:
            posts = await conn.fetch(
                """SELECT id, post_id, text, publish_date, attachments 
                FROM vkprod15_multiply_posts_timestamp 
                WHERE owner_id = $1 AND publish_date > $2""",
                int(owner_id), int(time.time())
            )

        old_times = [post['publish_date'] for post in posts]

        print(old_times)

        buttons = []

        for time1 in old_times:
            if time1 > time.time():

                formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time1))

                async with self.db.pool.acquire() as conn:

                    posts = await conn.fetch(
                        """SELECT text 
                        FROM vkprod15_multiply_posts_timestamp 
                        WHERE owner_id = $1 AND publish_date = $2""",
                        int(owner_id), time1
                    )

                    texts = [post['text'] for post in posts]

                    print(texts)

                    buttons.append([{
                        "action": {
                        "type": "text",
                        "label": f"{formatted_time} - {texts}",
                        "payload": '{"button": "statistics"}'
                        },
                        "color": "secondary"
                    }])

    keyboard = {
        "one_time": False,
        "inline": True,  #  inline keyboard
        "buttons": buttons
    }

    return json.dumps(keyboard, ensure_ascii=False)