from mistralai import Mistral
import os
from dotenv import load_dotenv
import re
import json

from classes import Clues, Response

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
          "content": """Créer un jeu 'Qui suis-je?' sur un sportif connu avec 5 indices numérotés en français,en anglais et en alemand.la réponse en JSON avec ce format
          {
            "reponse": "",
            "clues":[ 
            {
              "numero": 1,
              "francais": "",
              "anglais": "",
              "allemand": ""
            },
            {
              "numero": 2,
              "francais": "",
              "anglish": "",
              "allemand": ""
            },
            {
              "numero": 3,
              "francais": "",
              "anglish": "",
              "allemand": ""
            },
            {
              "numero": 4,
              "francais": "",
              "anglish": "",
              "allemand": ""
            },
            {
              "numero": 5,
              "francais": "",
              "anglish": "",
              "allemand": ""
            }
          ]
          }
          }""",
        },
    ],
    response_format = {
          "type": "json_object",
    }
)

response = chat_response.choices[0].message.content
try:
    json_loads = json.loads(response)
except json.JSONDecodeError as e:
    print(f"Erreur lors de la conversion du JSON: {e}")

print(json_loads)

clues_list = [Clues(**clue) for clue in json_loads['clues']]
response_data = Response(clues=clues_list, reponse=json_loads['reponse'])

print(response_data)