import requests
import os


class AIProvider:

    @staticmethod
    def openai(prompt: str, api_key: str = None):

        key = api_key or os.getenv("OPENAI_API_KEY")

        if not key:
            return "OpenAI API key missing"

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return f"OpenAI Error: {data}"


    @staticmethod
    def ollama(prompt: str):

        return "Ollama is not available on Render deployment"