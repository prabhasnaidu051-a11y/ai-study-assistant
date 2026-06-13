import requests
from openai import OpenAI


class AIProvider:

    @staticmethod
    def ollama(prompt):

        try:

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": False
                }
            )

            data = response.json()

            print("OLLAMA RESPONSE:", data)

            return data.get(
                "response",
                "No response from model"
            )

        except Exception as e:

            return (
                f"Ollama Error: {str(e)}"
            )

    @staticmethod
    def openai(
        prompt,
        api_key
    ):

        try:

            client = OpenAI(
                api_key=api_key
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return (
                response
                .choices[0]
                .message
                .content
            )

        except Exception as e:

            return (
                f"OpenAI Error: {str(e)}"
            )