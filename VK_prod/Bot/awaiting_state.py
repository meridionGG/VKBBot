async def handle_awaiting_state(self, user_id: int, message: str, attachments: str):

    state_data = self.awaiting_input[user_id]
    #user_data = self.user_sessions[user_id]

    if state_data["state"] == "awaiting_channel":
        await self.process_channel_input(self, user_id, message, state_data)

    elif state_data["state"] == "awaiting_channel_club":
        api_key = state_data["api_key"]
        await self.process_channel_club_input(self, user_id, message, api_key, state_data)

    elif state_data["state"] == "awaiting_existed_channel_club":
        api_key = state_data["api_key"]
        await self.process_existed_channel_club_input(self, user_id, message, api_key, state_data)

    elif state_data["state"] == "awaiting_channel_name":
        club_id = state_data["club_id"]
        await self.process_channel_name_input(self, user_id, message, club_id, state_data)

    elif state_data["state"] == "awaiting_post_text_channel":
        await self.process_post_text_channel(self, user_id, message, state_data)

    elif state_data["state"] == "awaiting_post_text":
        channel_id = state_data["channel_id"]
        channel_name = state_data["channel_name"]
        await self.process_post_text(self, user_id, message, channel_id, channel_name, state_data)

    elif state_data["state"] == "awaiting_post_attachments":
        channel_id = state_data["channel_id"]
        channel_name = state_data["channel_name"]
        print("im in awaiting-state", attachments)
        await self.process_publish_attachments(self, user_id, message, channel_id, state_data, channel_name, attachments)

    elif state_data["state"] == "awaiting_publish_time_day":
        channel_id = state_data["channel_id"] #channnel api_key
        text = state_data["text"] #text of post
        channel_name = state_data["channel_name"]
        link = state_data["link"]
        await self.process_publish_time_day(self, user_id, message, text, channel_id, channel_name, state_data, link)

    elif state_data["state"] == "awaiting_publish_time_time":
        time = state_data["timestamp"]
        text_day = state_data["publish_day"]
        channel_id = state_data["channel_id"] #channnel api_key
        text = state_data["text"] #text of post
        channel_name = state_data["channel_name"]
        link = state_data["link"]
        await self.process_publish_time_time(self, user_id, message, state_data, text_day, time, channel_id, text, channel_name, link)

    elif state_data["state"] == "awaiting_multiply_posts_text":
        await self.process_multiply_posts_text(self, user_id, message, state_data)

    elif state_data["state"] == "awaiting_process_multiply_posts_attachments":
        posts = state_data["posts"]
        print(posts)
        await self.process_multiply_posts_attachments(self, user_id, message, posts, attachments, state_data)

    elif state_data["state"] == "awaiting_process_multiply_posts_random":
        # posts = state_data["posts"]
        await self.process_multiply_posts_random(self, user_id, message, state_data)

    elif state_data["state"] == "awaiting_process_multiply_posts_time":
        answer = state_data["answer"]
        await self.process_multiply_posts_time(self, user_id, message, answer, attachments, state_data)