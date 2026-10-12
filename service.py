

import ollama


class ChatService:
    def __init__(self, model="llama3.2"):
        self.model = model

    def generate_stream(self, messages):
        response = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True,
        )

        for chunk in response:
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content