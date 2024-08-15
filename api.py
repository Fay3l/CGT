from mistralai import Mistral
import os
from dotenv import load_dotenv
from typing import List
import json
from PIL import Image, ImageDraw, ImageFont
from classes import Clues, Response, ContentData, TemplateData
from mistralai import Mistral
load_dotenv()


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

response_data = Response(clues=json_loads['clues'],name=json_loads['reponse'])


def create_instagram_story(template: List[TemplateData]):
    # Créer les images vierges
    for image in template:
        new_image = Image.new('RGB', (1080, 1920), color=(217, 217, 217))
        draw = ImageDraw.Draw(new_image)
        # Ajouter les textes à l'image
        for text in image.content:
            try:
                if(text.image):
                    foreground_image = Image.open(text.image)
                    foreground_image = foreground_image.resize((150, 150))  # Redimensionner si nécessaire    
                    position = (300, 200)
                font = ImageFont.truetype(font = text.fonts, size=text.font_size)
            except IOError:
                font = ImageFont.load_default()
                print(IOError)
            draw.text(text.position, text.clue_text, font=font, fill=text.color,align=text.align)
    # Enregistrer l'image
        new_image.save(image.path)

def open_instagram_story(content: List[ContentData]):
    # Créer les images vierges
        # Ajouter les textes à l'image
    for count,data in enumerate(content):
        if data.language == "fr":
            template = Image.open(f"./template/{data.language}/{count+1}.jpg")
            draw = ImageDraw.Draw(template)
        
        try:
            font = ImageFont.truetype(font = data.fonts, size=data.font_size)
        except IOError:
            font = ImageFont.load_default()
            print(IOError)
        
        draw.text(data.position, data.clue_text, font=font, fill=data.color,align=data.align)
        template.save(f"Clue_{count}_{data.language}.jpg")
    


print(response_data.clues)