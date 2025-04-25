import json

def create_publish_time_keyboard(self):
    """Создание клавиатуры, которая работает во всех клиентах"""
    keyboard = {
        "one_time": True,
        "inline": False,  # Обычная клавиатура (не inline)
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": "Сегодня",
                    "payload": "{\"button\": \"today\"}"
                },
                "color": "positive"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Завтра",
                    "payload": "{\"button\": \"tomorrow\"}"
                },
                "color": "secondary"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Послезавтра",
                    "payload": "{\"button\": \"day_after_tomorrow\"}"
                },
                "color": "secondary"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Отменить",
                    "payload": "{\"button\": \"settings\"}"
                },
                "color": "secondary"
            }],
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)