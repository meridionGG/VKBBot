import asyncpg


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self, **config):
        """Подключение к PostgreSQL"""
        self.pool = await asyncpg.create_pool(**config)
        await self._init_db()

    async def _init_db(self):
        """Создание таблиц"""
        async with self.pool.acquire() as conn:

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS vkprod9_channels (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,  -- Убрать UNIQUE
                session_id TEXT NOT NULL,
                channel_id TEXT,
                owner_id TEXT,
                channel_name TEXT
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS vkprod9_posts (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,  -- Убрать UNIQUE
                session_id TEXT NOT NULL,
                channel_id TEXT,
                channel_name TEXT,
                message_text TEXT,
                publish_time TEXT,
                is_published BOOLEAN
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS vkprod11_multiply_posts (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,  -- Убрать UNIQUE
                session_id TEXT NOT NULL,
                posts_text TEXT,
                photo_id TEXT,
                link TEXT,
                owner_id TEXT
                )
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS vkprod10_photos (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,  -- Убрать UNIQUE
                photo_id TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                session_id TEXT NOT NULL
                )
            ''')

    async def save_channel_id(self, user_id: int, channel_id: str, session_id: str):
        """Сохранение сообщения в БД"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO vkprod9_channels 
                    (user_id, session_id, channel_id)
                VALUES 
                    ($1, $2, $3)
        ''', user_id, session_id, channel_id)

    async def save_channel_club(self, user_id: int, club_id: str, api_key: str, session_id: str):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                 UPDATE vkprod9_channels
                 SET owner_id = $1
                 WHERE channel_id = $2
                ''', club_id, api_key)

    async def save_existed_channel_club(self, user_id: int, club_id: str, api_key: str, session_id: str):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                 INSERT INTO vkprod9_channels 
                    (user_id, session_id, channel_id, owner_id)
                VALUES 
                    ($1, $2, $3, $4)
                ''', user_id, session_id, api_key, club_id)

    async def save_channel_name(self, user_id: int, channel_name: str, club_id: str, session_id: str):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                 UPDATE vkprod9_channels
                 SET channel_name = $1
                 WHERE owner_id = $2
                ''', channel_name, club_id)


    async def save_message_text(self, user_id: int, text: str, channel_id: str, channel_name: str, session_id: str):
        """Сохранение сообщения в БД"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO vkprod9_posts
                (user_id, session_id, channel_id, channel_name, message_text)
                VALUES
                ($1, $2, $3, $4, $5)
                """, user_id, session_id, channel_id, channel_name, text
            )

    async def save_message_time(self, user_id: int, channel_id: str, message_text: str, text: str, session_id: str):
        """Сохранение сообщения в БД"""
        print(f"Im in database {message_text}")
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE vkprod9_posts
                SET publish_time = $1
                WHERE channel_id = $2 AND message_text = $3
                """, text, channel_id, message_text
            )

    async def update_timestamp(self, user_id: int, time_to_publish: str, published: bool):
        """Сохранение сообщения в БД"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE vkprod9_posts
                SET is_published = $1
                WHERE user_id = $2 AND publish_time = $3
                """, published, user_id, time_to_publish
            )

    async def save_posts_text(self, user_id: int, posts: str, session_id: str):
        """Сохранение сообщения в БД"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO vkprod11_multiply_posts
                (user_id, posts_text, session_id)
                VALUES
                ($1, $2, $3)
                """, user_id, posts, session_id
            )

    async def save_multiply_attachments(self, user_id: int, photo_id: str, owner_id: str, posts_text, link):
        """Сохранение сообщения в БД"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE vkprod11_multiply_posts
                SET photo_id = $1, owner_id = $2, link = $3
                WHERE user_id = $4 AND posts_text = $5
                """, photo_id, owner_id, link, user_id, posts_text)

    async def save_photos(self, user_id: int, photo_id: str, owner_id: str, session_id: str):
        """Сохранение сообщения в БД"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO vkprod10_photos
                (user_id, photo_id, owner_id, session_id)
                VALUES
                ($1, $2, $3, $4)
                """, user_id, photo_id, owner_id, session_id
            )

    async def close(self):
        """Закрытие соединения"""
        await self.pool.close()