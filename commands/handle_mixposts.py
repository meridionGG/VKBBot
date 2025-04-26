import random
import time


async def handle_mixposts(self, user_id: int):
    async with self.db.pool.acquire() as conn:
        # Получаем все каналы пользователя
        channels = await conn.fetch(
            "SELECT channel_id, owner_id FROM vkprod11_channels WHERE user_id = $1",
            user_id
        )

    if not channels:
        await self.send_message(
            user_id,
            f"У вас нет доступных каналов. Добавьте используя 'Мои каналы'",
            keyboard=self.create_keyboard(self)
        )
        return

    i = 0
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

        if not posts:
            await self.send_message(
                user_id,
                f"Нет запланированных постов.",
                keyboard=self.create_keyboard(self)
            )
            break

            # Собираем данные
        post_ids = [post['post_id'] for post in posts]  # ID постов в VK (для удаления)
        db_ids = [post['id'] for post in posts]  # ID записей в БД
        texts = [post['text'] for post in posts]
        old_times = [post['publish_date'] for post in posts]
        attachments = [post['attachments'] for post in posts]

            # Перемешиваем времена
        shuffled_times = random.sample(old_times, len(old_times))

        async with self.db.pool.acquire() as conn:
            channels_id = await conn.fetch("SELECT channel_id FROM vkprod11_channels WHERE user_id = $1",
                                            user_id)

            channel_names = await conn.fetch("SELECT channel_name FROM vkprod11_channels WHERE user_id = $1",
                                           user_id)

        all_channels = [record['channel_id'] for record in channels_id]
        all_channel_names = [record['channel_name'] for record in channel_names]

        decrypted_binary_channel_id = self.f.decrypt(all_channels[0])
        decrypted_channel_id = decrypted_binary_channel_id.decode('utf-8')
        # print(f"Encrypted token - {token}")
        print(f"Decrypted token - {decrypted_channel_id} with type of - {type(decrypted_channel_id)}")

        await self.update_token(
            new_token=decrypted_channel_id
        )

            # Удаляем старые посты из VK
        for post_id in post_ids:
            await self.delete_post_wall(owner_id=int(owner_id), post_id=post_id)
            print(f"Удалён пост {post_id} в канале {owner_id}")

            # Публикуем новые посты с новыми временами
        for db_id, text, new_time, attach in zip(db_ids, texts, shuffled_times, attachments):
                # Отправляем пост в VK
            post_id = await self.post_to_wall(
                user_id=user_id,
                text=text,
                publish_date=new_time,
                owner_id=int(owner_id),
                attachments=attach
            )

            async with self.db.pool.acquire() as conn:
                await conn.execute(
                    """UPDATE vkprod15_multiply_posts_timestamp
                    SET post_id = $1, publish_date = $2
                    WHERE id = $3""",
                    post_id, new_time, db_id
                )

                print(f"Опубликован пост {post_id} на время {new_time}")

        await self.send_message(
            user_id,
            f"Посты успешно перемешаны для {all_channel_names[i]}",
            keyboard=self.create_keyboard(self)
        )
        i += 1

    # await self.send_message(
    #     user_id,
    #     f"Посты успешно перемешаны и отправлены.",
    #     keyboard=None
    # )

    await self.wall_session.close()