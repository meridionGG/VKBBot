import asyncio

import aiovk
from aiovk import API, TokenSession
from aiovk.longpoll import BotsLongPoll

async def post_to_wall(user_id: int, text: str, publish_date: int, channel_id: str, keyboard=None):
    # Initialize the session with your access token

    wall_session = aiovk.TokenSession(channel_id)
    wall_api = aiovk.API(wall_session)

    owner_id = -int(user_id)
    print(type(publish_date))
    # Parameters for the post
    params = {
        'owner_id': -229907109,
        'from_group': 0,
        'message': text,
        'publish_date': publish_date,
    }
    print("Я в main")

    try:
        response = await wall_api.wall.post(**params)
        print("Post successfully published! Post ID:", response['post_id'])
        # if response:
        # await self.check_publish_time(self, user_id, publish_date)
    except Exception as e:
        print("Error:", e)

    return True