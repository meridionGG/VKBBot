import json

def create_multiply_posts_keyboard(self):
    """Создание клавиатуры, которая работает во всех клиентах"""
    keyboard = {
        "one_time": False,
        "inline": False,  #Inline keyboard
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "label": "Подтвердить",
                    "payload": "{\"button\": \"new_posts\"}"
                },
                "color": "positive"
            }],
            [{
                "action": {
                    "type": "text",
                    "label": "Отменить",
                    "payload": "{\"button\": \"my_channels\"}"
                },
                "color": "secondary"
            }]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)