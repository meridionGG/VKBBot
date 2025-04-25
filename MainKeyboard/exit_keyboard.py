import json

def exit_keyboard(self):
    """Создание клавиатуры, которая работает во всех клиентах"""
    keyboard = {
        "one_time": False,
        "inline": False,  # Обычная клавиатура (не inline)
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": "Отмена",
                    "payload": "{\"button\": \"new_posts\"}"
                },
                "color": "negative"
            }],
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)