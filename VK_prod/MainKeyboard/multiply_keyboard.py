import json

def create_multiply_keyboard(self):
    """Создание клавиатуры, которая работает во всех клиентах"""
    keyboard = {
        "one_time": False,
        "inline": False,  # Обычная клавиатура (не inline)
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": "Далее",
                    "payload": "{\"button\": \"one_post\"}"
                },
                "color": "positive"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Отменить",
                    "payload": "{\"button\": \"back\"}"
                },
                "color": "secondary"
            }],
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)