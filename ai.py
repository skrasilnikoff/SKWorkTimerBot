from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


class AI_Bot:
    def __init__(self, base_url, api_key):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.prev_text = ''
        self.history = []

    def _save_to_history(self, message, role):
        self.history.append({"role": role, "content": message})

    def _get_prompt(self, prev_text):
        print('prev_text', prev_text)
        prompt = f"""
        Вас зовут Олег, вы мужчина, и вы являетесь русскоязычным помощником по умолчанию.  
        Если пользователь попросит вас ответить на другом языке, вы должны сделать это.
        """

        self._save_to_history(prev_text, "user")

        # print("prompt", prompt)

        return prompt

    def generate_response(self, text):
        lower_text = text.lower()
        if 'олег' not in lower_text:
            return ''
        prompt = self._get_prompt(self.prev_text)
        completion = self.client.chat.completions.create(
            model="gemma-2-2b-it",
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
