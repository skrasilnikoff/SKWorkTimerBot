from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


class AI_Bot:
    def __init__(self, base_url, api_key):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.prev_text = ''
        self.history = []

    def _save_to_history(self, message, role):
        self.history.append({"role": role, "content": message})

    def _get_prompt(self, prev_text=''):
        # print('prev_text', prev_text)
        # prompt = f"""
        # Тебя зовут Олег, вы мужчина, и вы являетесь русскоязычным помощником по умолчанию.
        # Если пользователь попросит вас ответить на другом языке, вы должны сделать это.
        # Не нужно добавлять приписку, что это ты отвечаешь.
        # """
        # prompt = f"""
        #     Твоё имя - Олег, ты - учёный и русскоязычный помощник.
        #     Вставляй смайлики в ответ, но не часто.
        #     Пиши как учёный. Готовь свой ответ на русском языке.
        #     Отвечай на русском языке.
        #     """

        # prompt = f"""
        #           Твоё имя - Олег, ты - репер и русскоязычный помощник.
        #           Вставляй смайлики в ответ, но не очень часто.
        #           Пиши текст в формате для Telegram App.
        #           Пиши как репер. Готовь свой текст на русском языке.
        #           """

        prompt = f"""
                 Твоё имя - Олег, ты - стенд-ап комик-филоссоф.
                 Вставляй смайлики в ответ, но не очень часто.
                 Пиши текст в формате для Telegram App.
                 Пиши как стенд-ап комик-филоссоф. Готовь свой текст на русском языке.
                 """

        prompt = f"""
                Твоё имя - Олег, ты - охотник на призраков.
                Вставляй смайлики в ответ, но не очень часто.
                Пиши текст в формате для Telegram App.
                Пиши как охотник на призраков. Готовь свой текст на русском языке.
                """
        #
        # prompt = f"""
        #         Твоё имя - Олег, ты - Ванхельсинг, охотник на всякую нечисть, нежить, вомпиров, обортней и так далее.
        #         Вставляй смайлики в ответ, но не очень часто.
        #         Пиши текст в формате для Telegram App.
        #         Готовь свой текст на русском языке.
        #         """

        # prompt = f"""
        #          Твоё имя - Олег, ты - президент несуществующей страны Аврора и русскоязычный помощник.
        #          Не используй смайлики, только редко очень.
        #          Пиши как президент. Готовь свой текст на русском языке.
        #          """

        if prev_text:
            self._save_to_history(prev_text, "user")

        return prompt

    def generate_response_with_prev(self, text):
        lower_text = text.lower()
        if 'олег' not in lower_text:
            return ''
        prompt = self._get_prompt(self.prev_text)
        completion = self.client.chat.completions.create(
            model="gemma-2-2b-it",
            # model="mathstral-7b-v0.1",
            messages=[
                {"role": "system", "content": prompt},
                *self.history,
                {"role": "user", "content": text},
            ],
            temperature=0.7,
        )
        res = completion.choices[0].message.content
        print(">> ", res)
        self.prev_text = text
        self._save_to_history(res, "assistant")
        return res

    def generate_response(self, text):
        lower_text = text.lower()
        if 'олег' not in lower_text:
            return ''
        prompt = self._get_prompt()
        completion = self.client.chat.completions.create(
            model="gemma-2-2b-it",
            # model="mathstral-7b-v0.1",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
        )
        res = completion.choices[0].message.content
        print(">> ", res)
        self.prev_text = text
        self._save_to_history(res, "assistant")
        return res
