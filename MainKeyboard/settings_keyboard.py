import json

async def create_settings_keyboard(self, user_id):

    async with self.db.pool.acquire() as conn:
        time_zone = await conn.fetch("SELECT timezone FROM vkprod10_timezone WHERE user_id = $1",
                                   user_id)

    all_time_zones = [record['timezone'] for record in time_zone]
    if all_time_zones == []:
        time_zone = "+3" #по стандарту стоит МСК
    else:
        time_zone = all_time_zones[-1]
    print(f"Timezone in db {time_zone}")

    """Создание клавиатуры, которая работает во всех клиентах"""
    keyboard = {
        "one_time": True,
        "inline": False,  # Обычная клавиатура (не inline)
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": f"Часовой пояс [GMT {time_zone}]",
                    "payload": "{\"button\": \"timestamp\"}"
                },
                "color": "secondary"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Перемешать посты",
                    "payload": "{\"button\": \"mix_posts\"}"
                },
                "color": "secondary"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Отмена",
                    "payload": "{\"button\": \"cancel\"}"
                },
                "color": "negative"
            }],
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)