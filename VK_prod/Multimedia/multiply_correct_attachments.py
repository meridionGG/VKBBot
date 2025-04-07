import requests
from pathlib import Path
import os
import aiovk

# Абсолютный путь к папке для загрузок
DOWNLOAD_DIR = Path("/home/ss/PycharmProjects/VK_prod/Downloads")

async def multiply_correct_attachments(self, user_id, session_id, post, link):

    async with self.db.pool.acquire() as conn:
        channels = await conn.fetch("SELECT channel_id FROM vkprod9_channels WHERE user_id = $1",
                                   user_id)

        all_channels = [record['channel_id'] for record in channels]
        result = all_channels[0]

    await get_url_to_post(self, result, user_id, session_id, post, link)

async def get_url_to_post(self, result, user_id, session_id, post, link):
        # Initialize the session with your access token
    async with aiovk.TokenSession(
            access_token=result) as session:
        vk = aiovk.API(session)

        try:
            response = await vk.photos.getWallUploadServer()
            url = response["upload_url"]
            print(response)
        except aiovk.exceptions.VkAPIError as e:
            print("Error:", e)
        await download_image_to_url(self, url, result, user_id, session_id, post, link)

async def download_image_to_url(self, url, result, user_id, session_id, post, link):

    for filename in os.listdir(DOWNLOAD_DIR):
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        if os.path.isfile(filepath):  # Проверяем, что это файл, а не папка
            print(f"Найден файл: {filename}")
            print(f"Полный путь: {filepath}")

            files = {
                'photo': open(filepath, 'rb'),
            }
            response = requests.post(f'{url}', files=files)

            photo_data = response.json()['photo']
            server = response.json()['server']
            hash = response.json()['hash']

            print(response.json())
            print("im in download_image_to_url")
            print(photo_data)
            os.remove(filepath)

            await save_image_on_vk(self, photo_data, server, hash, result, user_id, session_id, post, link)

async def save_image_on_vk(self, photo_data, server, hash, result, user_id, session_id, post, link):
    async with aiovk.TokenSession(
            access_token=result) as session:
        vk = aiovk.API(session)
        print(type(server))

        params = {
             'photo': photo_data,
             'server': server,
             'hash': hash
        }

        try:
            response = await vk.photos.saveWallPhoto(**params)
            print(response)
        except aiovk.exceptions.VkAPIError as e:
            print("Error:", e)

    photo_id = response[0]['id']
    owner_id = response[0]['owner_id']

    await self.db.save_multiply_attachments(
        user_id=user_id,
        photo_id=str(photo_id),  # vk_api_key
        owner_id=str(owner_id),
        posts_text=post,
        link=link
    )