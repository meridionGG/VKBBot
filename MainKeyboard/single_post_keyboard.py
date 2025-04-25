import json
import time

async def single_post_keyboard(self, user_id):
    """Создание клавиатуры, которая работает во всех клиентах"""

    buttons = []

    async with self.db.pool.acquire() as conn:
        # Получаем все каналы пользователя
        channel_ids = await conn.fetch("SELECT channel_name FROM vkprod11_channels WHERE user_id = $1",
                                       user_id)

        all_channel_ids = [record['channel_name'] for record in channel_ids]
        print(f"These {all_channel_ids}")

    if str(channel_ids) == '[]':
        await self.send_message(
            user_id,
            "У вас нет доступных каналов. Добавьте используя 'Мои каналы'.",
            keyboard=self.create_keyboard(self)
        )
    else:
        for channel in all_channel_ids:
            buttons.append([{
                "action": {
                "type": "text",
                "label": f"{channel}",
                "payload": '{"button": "channel"}'
                },
                "color": "secondary"
            }])

    keyboard = {
        "one_time": False,
        "inline": True,  #  inline keyboard
        "buttons": buttons
    }

    return json.dumps(keyboard, ensure_ascii=False)