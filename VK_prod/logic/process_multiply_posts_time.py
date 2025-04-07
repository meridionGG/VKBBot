from datetime import datetime, timezone, timedelta
import re
import random

posts = []

async def process_multiply_posts_time(self, user_id: int, message: str, answer, attachments, state_data: dict):
    await self.send_message(
        user_id,
        f"Посты успешно загружены. Выберите время публикации в формате ЧЧ:ММ, в одном сообщении с новой строки.",
        keyboard=None
    )

    print(message)
    session_id = state_data["session_id"]

    records = message.split('\n')

    if answer == "Нет":

        # await self.send_message(
        #     user_id,
        #     f"Посты успешно загружены. Выберите время публикации в формате ЧЧ:ММ, в одном сообщении с новой строки.",
        #     keyboard=None
        # )

        for i in range(len(records)):
            print(records)

            if await is_valid_time(records[i]) == True:

                time = await subtract_hours(records[i], 3)

                utc_time = datetime.now(timezone.utc)
                utc_time_date = str(utc_time.date())
                time_today = utc_time_date + " " + time + ":00"
                print(time_today)
                publish_date_timestamp = datetime.strptime(time_today, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                publish_date_timestamp_unix = int(publish_date_timestamp.timestamp())

                async with self.db.pool.acquire() as conn:
                    message = await conn.fetch("SELECT posts_text FROM vkprod11_multiply_posts WHERE session_id = $1",
                                               session_id)

                    all_messages = [record['posts_text'] for record in message]
                    result_message = all_messages[i]

                    owners_id = await conn.fetch("SELECT owner_id FROM vkprod9_channels WHERE user_id = $1",
                                                 user_id)

                    channels_id = await conn.fetch("SELECT channel_id FROM vkprod9_channels WHERE user_id = $1",
                                                   user_id)

                    photos = await conn.fetch(
                        "SELECT photo_id, owner_id FROM vkprod11_multiply_posts WHERE user_id = $1 AND session_id = $2 AND posts_text = $3",
                                                   user_id, session_id, result_message)

                    photo_strings = [f"photo{record['owner_id']}_{record['photo_id']}" for record in photos]

                    attachments = ", ".join(photo_strings)

                    all_channels = [record['channel_id'] for record in channels_id]

                    # all_messages = [record['posts_text'] for record in message]
                    # result_message = all_messages[i]

                    print(result_message)
                    all_owner_ids = [record['owner_id'] for record in owners_id]

                    for j in range(len(all_owner_ids)):
                        result_owner_id = all_owner_ids[j]
                        print(result_owner_id)

                        await self.update_token(
                            new_token=all_channels[0]
                        )

                        await self.post_to_wall(
                            user_id=user_id,
                            owner_id=int(result_owner_id),
                            text=result_message,
                            attachments=attachments,
                            publish_date=publish_date_timestamp_unix
                        )

        await self.send_message(
            user_id,
            f"Посты успешно отправлены.",
            keyboard=None
        )

        del self.awaiting_input[user_id]
        del self.user_sessions[user_id]

    # else:
    #
    #     await self.send_message(
    #         user_id,
    #         f"Не понял ваше действие, введите еще раз.",
    #         None
    #     )


    elif answer == "Да":

        # await self.send_message(
        #     user_id,
        #     f"Посты успешно загружены. Выберите время публикации в формате ЧЧ:ММ, в одном сообщении с новой строки.",
        #     keyboard=None
        # )

        async with self.db.pool.acquire() as conn:

            owners_id = await conn.fetch("SELECT owner_id FROM vkprod9_channels WHERE user_id = $1",
                                         user_id)

            all_owner_ids = [record['owner_id'] for record in owners_id]


        for i in range(len(all_owner_ids)):

            result_owner_id = all_owner_ids[i]
            print(result_owner_id)

            for j in range(len(records)):

                random_time = random.choice(records)

                if await is_valid_time(random_time) == True:

                    time = await subtract_hours(random_time, 3)
                    print(time)

                    utc_time = datetime.now(timezone.utc)
                    utc_time_date = str(utc_time.date())
                    time_today = utc_time_date + " " + time + ":00"
                    print(time_today)
                    publish_date_timestamp = datetime.strptime(time_today, "%Y-%m-%d %H:%M:%S").replace(
                        tzinfo=timezone.utc)
                    publish_date_timestamp_unix = int(publish_date_timestamp.timestamp())

                    async with self.db.pool.acquire() as conn:
                        message = await conn.fetch("SELECT posts_text FROM vkprod11_multiply_posts WHERE session_id = $1",
                                                session_id)

                        all_messages = [record['posts_text'] for record in message]
                        result_message = all_messages[j]

                        channels_id = await conn.fetch("SELECT channel_id FROM vkprod9_channels WHERE user_id = $1",
                                                    user_id)

                        photos = await conn.fetch(
                            "SELECT photo_id, owner_id FROM vkprod11_multiply_posts WHERE user_id = $1 AND session_id = $2 AND posts_text = $3",
                                                        user_id, session_id, result_message)

                        photo_strings = [f"photo{record['owner_id']}_{record['photo_id']}" for record in photos]

                        attachments = ", ".join(photo_strings)

                        all_channels = [record['channel_id'] for record in channels_id]

                # all_messages = [record['posts_text'] for record in message]
                # result_message = all_messages[i]
                        print(result_message)

                        await self.update_token(
                        new_token=all_channels[0]
                        )

                        await self.post_to_wall(
                            user_id=user_id,
                            owner_id=int(result_owner_id),
                            text=result_message,
                            attachments=attachments,
                            publish_date=publish_date_timestamp_unix
                        )

            await self.send_message(
                user_id,
                f"Посты успешно отправлены.",
                keyboard=None
            )

        del self.awaiting_input[user_id]
        del self.user_sessions[user_id]



async def is_valid_time(time_str):
    pattern = r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.fullmatch(pattern, time_str))

async def subtract_hours(time_str, hours_to_subtract):
    hours, minutes = map(int, time_str.split(':'))

    hours = (hours - hours_to_subtract) % 24
    return f"{hours:02d}:{minutes:02d}"
