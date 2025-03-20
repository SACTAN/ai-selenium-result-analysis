import os
from groq import Groq

class ChatGroq:
    def __init__(self, model: str, temperature: float = 0.5, api_key: str = None, **kwargs):
        if api_key is None:
            raise ValueError("GROQ_API_KEY must be provided")
        self.model = model
        self.temperature = temperature
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        # Ensure prompt is a string
        prompt = str(prompt)
        # Provide a basic system message for context
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=self.temperature
        )
        return response.choices[0].message.content

    def __call__(self, prompt: str) -> str:
        return self.generate(prompt)
