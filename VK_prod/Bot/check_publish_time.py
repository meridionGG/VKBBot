import time
import asyncio

async def check_publish_time(self, user_id: int, time_to_publish: int):
    print("aaaaaaaaaaaaaaasalamaleykum")
    while True:
        current_timestamp = int(time.time())
        if current_timestamp >= time_to_publish:
            print("I did it")
            await self.db.update_timestamp(
                user_id=user_id,
                time_to_publish=str(time_to_publish),
                published=True
            )
            break
        await asyncio.sleep(30)