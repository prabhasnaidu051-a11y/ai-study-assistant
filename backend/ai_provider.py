import os
from groq import Groq


class AIProvider:

    @staticmethod
    def groq(prompt: str):

        key = os.getenv("GROQ_API_KEY")

        if not key:
            return "GROQ API key missing"

        client = Groq(
            api_key=key
        )

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )


        return response.choices[0].message.content



    @staticmethod
    def openai(prompt: str, api_key: str = None):

        return "OpenAI disabled. Use Groq free API."



    @staticmethod
    def ollama(prompt: str):

        return "Ollama is not available on Render"