import json

def create_new_post_keyboard(self):
    """Создание клавиатуры, которая работает во всех клиентах"""
    keyboard = {
        "one_time": False,
        "inline": False,  # Обычная клавиатура (не inline)
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": "Один пост",
                    "payload": "{\"button\": \"one_post\"}"
                },
                "color": "positive"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Подборка постов",
                    "payload": "{\"button\": \"few_posts\"}"
                },
                "color": "secondary"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Назад",
                    "payload": "{\"button\": \"back\"}"
                },
                "color": "secondary"
            }],
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)