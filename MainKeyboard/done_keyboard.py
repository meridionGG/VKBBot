import json

def create_done_keyboard(self):
    """Создание клавиатуры, которая работает во всех клиентах"""
    keyboard = {
        "one_time": False,
        "inline": False,  # Обычная клавиатура (не inline)
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": "Завершить",
                    "payload": "{\"button\": \"few_posts\"}"
                },
                "color": "secondary"
            }],

        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)