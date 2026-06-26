# pylint: disable=too-few-public-methods

import requests


class AIProvider:


    @staticmethod
    def openai(prompt: str, api_key: str):

        response = requests.post(

            "https://api.openai.com/v1/chat/completions",

            headers={

                "Authorization": f"Bearer {api_key}",

                "Content-Type": "application/json"

            },

            json={

                "model": "gpt-4o-mini",

                "messages":[

                    {

                        "role":"user",

                        "content":prompt

                    }

                ]

            },

            timeout=60

        )


        data = response.json()


        if "choices" in data:

            return data["choices"][0]["message"]["content"]


        return f"OpenAI Error: {data}"