from datetime import datetime, timezone, timedelta
from Bot.post_to_wall import post_to_wall
from Bot.var import wall_post_access_token
import re
import time

async def process_publish_time_time(self, user_id: int, message: str, state_data: dict, text_day: str, channel_name, link):
    #channel_id взять из vkprod10_channels и расшифровать
    global publish_date_timestamp_unix
    session_id = state_data["session_id"]
    time_today = text_day
    print(time_today)
    print(message)

    async with self.db.pool.acquire() as conn:
        time_zone = await conn.fetch("SELECT timezone FROM vkprod10_timezone WHERE user_id = $1",
                                   user_id)

    all_time_zones = [record['timezone'] for record in time_zone]
    print(all_time_zones)

    if all_time_zones == []:
        time_zone = "+3" #по стандарту стоит МСК
    else:
        time_zone = all_time_zones[-1]

    print(f"Timezone in db {time_zone}")

    if await is_valid_time(message) == True:

        time1 = await subtract_hours(message, time_zone)

        if text_day == "Сегодня":
            utc_time = datetime.now(timezone.utc)
            utc_time_date = str(utc_time.date())
            time_today = utc_time_date + " " + time1 + ":00"
            print(time_today)
            publish_date_timestamp = datetime.strptime(time_today, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            publish_date_timestamp_unix = int(publish_date_timestamp.timestamp())


        elif text_day == "Завтра":
            utc_time = datetime.now(timezone.utc)
            utc_time_date = str(utc_time.date()+ timedelta(days=1))
            time_tomorrow = utc_time_date + " " + time1 + ":00"
            print(time_tomorrow)
            publish_date_timestamp = datetime.strptime(time_tomorrow, "%Y-%m-%d %H:%M:%S")
            publish_date_timestamp_unix = int(publish_date_timestamp.timestamp())


        elif text_day == "Послезавтра":
            utc_time = datetime.now(timezone.utc)
            utc_time_date = str(utc_time.date() + timedelta(days=2))
            time_after_tomorrow = utc_time_date + " " + time1 + ":00"
            print(time_after_tomorrow)
            publish_date_timestamp = datetime.strptime(time_after_tomorrow, "%Y-%m-%d %H:%M:%S")
            publish_date_timestamp_unix = int(publish_date_timestamp.timestamp())

        print(publish_date_timestamp_unix)

        if publish_date_timestamp_unix > time.time():

            try:
                # Сохраняем в базу данных
                # await self.db.save_message_time(
                #     user_id=user_id,
                #     channel_id=channel_id, #vk_api_key
                #     message_text=text, #Текст поста
                #     text=str(publish_date_timestamp_unix), # unix timestamp
                #     session_id=state_data["session_id"],
                # )

                async with self.db.pool.acquire() as conn:

                    channel_ids = await conn.fetch("SELECT channel_id FROM vkprod11_channels WHERE user_id = $1",
                                                user_id)

                    all_channel_ids = [record['channel_id'] for record in  channel_ids]

                    channel_id = all_channel_ids[0]

                    message = await conn.fetch("SELECT message_text FROM vkprod10_posts WHERE user_id = $1 AND session_id = $2",
                                                user_id, session_id)

                    club = await conn.fetch("SELECT owner_id FROM vkprod11_channels WHERE channel_id = $1 AND channel_name = $2",
                                                channel_id, channel_name)

                    photos = await conn.fetch("SELECT photo_id, owner_id FROM vkprod10_photos WHERE user_id = $1 AND session_id = $2",
                                                user_id, session_id)

                    photo_strings = [f"photo{record['owner_id']}_{record['photo_id']}" for record in photos]
                    attachments = ", ".join(photo_strings)
                # print(f"Photo ID: {photo['photo_id']}, Owner ID: {photo['owner_id']}")
                # photo_id = str(photo['photo_id'])
                # owner_id = str(photo['owner_id'])


                    all_messages = [record['message_text'] for record in message]
                    print(all_messages)
                    result = all_messages[0]
                    club_id = [record['owner_id'] for record in club]
                    club_id = club_id[0]
                    print(club_id)
                    print("Я тут")
                    print(result)

                    print(publish_date_timestamp_unix)

                    await self.db.save_message_time(
                        user_id=user_id,
                        channel_id=club_id,
                        message_text=result,
                        publish_date=publish_date_timestamp_unix
                    )

                    decrypted_binary_channel_id = self.f.decrypt(channel_id)
                    decrypted_channel_id = decrypted_binary_channel_id.decode('utf-8')
                    # print(f"Encrypted token - {token}")
                    print(f"Decrypted token - {decrypted_channel_id} with type of - {type(decrypted_channel_id)}")

                    await self.update_token(
                        new_token=decrypted_channel_id #vkapi Token
                    )

                    if link != None:
                        link = link
                        attachments = attachments+', '+link
                    else:
                        attachments = attachments

                    await self.post_to_wall(
                        user_id=user_id,
                        text=result,
                        owner_id=int(club_id),
                        publish_date=publish_date_timestamp_unix,
                        attachments=attachments
                    )

                    await self.send_message(
                        user_id,
                        f"Пост успешно отправлен.",
                        self.create_keyboard(self)
                    )

                    print("Дошел")

                    del self.awaiting_input[user_id]
                    del self.user_sessions[user_id]

            except Exception as e:
                print("Error:", e)

        else:
            await self.send_message(
                user_id,
                f"Неверно ввели время публикации. Проверьте на соответствие с ЧЧ:ММ.",
            )

    # del self.awaiting_input[user_id]
    # del self.user_sessions[user_id]
    #session_id = self.user_sessions[user_id]["session_id"]
async def is_valid_time(time_str):
    pattern = r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.fullmatch(pattern, time_str))

async def subtract_hours(time_str, hours_to_subtract):
    hours, minutes = map(int, time_str.split(':'))

    if "+" in hours_to_subtract:
        hours_to_subtract = int(hours_to_subtract.replace("+", ""))
        hours = (hours - hours_to_subtract) % 24
    else:
        hours_to_subtract = int(hours_to_subtract.replace("-", ""))
        hours = (hours + hours_to_subtract) % 24
    return f"{hours:02d}:{minutes:02d}"