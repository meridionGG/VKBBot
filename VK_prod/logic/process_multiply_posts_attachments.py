from datetime import datetime, timezone, timedelta

attachments_list = []
links_list = []

async def process_multiply_posts_attachments(self, user_id: int, message: str, answer, attachments, state_data: dict,):

    print("state data")
    print(message)
    print(state_data)
    session_id = state_data["session_id"]

    if message == "Да":
        await self.send_message(
            user_id,
            "Можете отправлять фотографии по 1 штуке. По завершении нажмите на кнопку 'Далее', чтобы перейти к заполнению следующего поста, 'Отменить', чтобы вернуться в главное меню.",
            keyboard=self.create_multiply_keyboard(self)
        )

    elif attachments != None:
        print('im in process_publish_attachments')
        print(attachments)
        attachments_list.append(attachments)

    elif message != "Далее" and message != "Нет":
        links_list.append(message)

    elif message == "Далее":

        print(attachments_list)

        if links_list:
            link = links_list[0]
        else:
            link = None

        await self.multiply_loader(self, attachments_list, user_id, session_id, posts, link)

        attachments_list.clear()
        links_list.clear()

        await self.send_message(
            user_id,
            "Все медиаматериалы успешно загружены. Если хотите ввести текст для нового поста, то введите его: ",
            self.create_done_keyboard(self)
        )

        self.awaiting_input[user_id] = {
            "state": "awaiting_multiply_posts_text",
            "session_id": state_data["session_id"]
        }

    elif message == "Нет":
        print("дошел")

        await self.send_message(
            user_id,
            "✅ Пост сохранен без медиаматериалов! Если хотите ввести текст для нового поста, то введите его: ",
            self.create_done_keyboard(self)
        )

        print(f"Должно вывестить НЕТ {message}")

        self.awaiting_input[user_id] = {
            "state": "awaiting_multiply_posts_text",
            "session_id": state_data["session_id"],
        }
