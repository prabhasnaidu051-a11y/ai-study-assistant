# pylint: disable=too-few-public-methods
import requests


class AIProvider:

    @staticmethod
    def ollama(prompt: str):

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        data = response.json()

        if "response" in data:
            return data["response"]

        return f"Ollama Error: {data}"
