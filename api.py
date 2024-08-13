from mistralai import Mistral
import os
from dotenv import load_dotenv
import re

load_dotenv()
from mistralai import Mistral

api_key = os.getenv("MISTRALAPI_KEY")
model = "open-mistral-7b"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": f"Créer un jeu 'Qui suis-je?' sur un sportif connu avec 5 indices numérotés.Traduire en anglais et allemand. Donné la réponse",
        },
    ]
)

response = chat_response.choices[0].message.content

indices = re.findall(r'\d+\.\s*(.+)', response)

for i, indice in enumerate(indices, start=1):
    print(f"{i}. {indice}")