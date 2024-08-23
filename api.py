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

def create_template_clues(content: ContentData):
    # Créer les images vierges
        # Ajouter les textes à l'image
      if content.language == "fr":
          template = Image.open(f"./template/{content.language}/{content.clue_number}.jpg")
          draw = ImageDraw.Draw(template)
      
      try:
          font = ImageFont.truetype(font = content.fonts, size=content.font_size)
      except IOError:
          font = ImageFont.load_default()
          print(IOError)
      
      draw.text(content.position, content.clue_text, font=font, fill=content.color,align=content.align)
      template.save(f"Clue_{content.clue_number}_{content.language}.jpg")

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
              "anglais": "",
              "allemand": ""
            },
            {
              "numero": 3,
              "francais": "",
              "anglais": "",
              "allemand": ""
            },
            {
              "numero": 4,
              "francais": "",
              "anglais": "",
              "allemand": ""
            },
            {
              "numero": 5,
              "francais": "",
              "anglais": "",
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


for content in response_data.clues:
  content_data = ContentData(clue_text=content["francais"], position=(100,800), font_size=70 , color=(0,0,0), align="center", fonts="./fonts/Sans.ttf",language="fr",clue_number=content["numero"])
  create_template_clues(content_data)


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


    


