import json

def attachments_keyboard(self):
    """Создание клавиатуры, которая работает во всех клиентах"""
    keyboard = {
        "one_time": False,
        "inline": True,  # Обычная клавиатура (не inline)
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": "Да",
                    "payload": "{\"button\": \"yes\"}"
                },
                "color": "positive"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Нет",
                    "payload": "{\"button\": \"no\"}"
                },
                "color": "secondary"
            }],
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)