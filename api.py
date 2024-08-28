from mistralai import Mistral
import os
from dotenv import load_dotenv
import json
from PIL import Image, ImageDraw, ImageFont
from classes import Response, ContentData
load_dotenv()


api_key = os.getenv("MISTRALAPI_KEY")
client_key = os.getenv("CLIENT_KEY")
client_secret =os.getenv("CLIENT_SECRET")
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
    # Diviser le texte en mots
    words = content.clue_text.split()
    lines = []
    current_line = []
    box_width, box_height = template.size
    max_width = box_width * 0.9  # Laisser un peu de marge

    for word in words:
        test_line = ' '.join(current_line + [word])
        line_width, _ = draw.textbbox((0, 0), test_line, font=font)[2:4]
        if line_width > max_width:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))

    # Calculer la taille de chaque ligne
    line_heights = [draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines]
    total_height = sum(line_heights)

    # Calculer la position centrale verticale
    y_start = (box_height - total_height) // 2

    # Ajouter chaque ligne à l'image
    for i, line in enumerate(lines):
        line_width = draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]
        x = (box_width - line_width) // 2
        y = y_start + sum(line_heights[:i])
        draw.text((x, y), line, font=font, fill=content.color)
    template.save(f"./upload/{content.language}/Clue_{content.clue_number}_{content.language}.jpg")
    # Supposons que res est votre image et content.response est votre texte
    res = Image.open(f"./template/{content.language}/10.jpg")
    draw_res = ImageDraw.Draw(res)

    # Calculer le point central de l'image
    center_x = res.width // 2
    center_y = res.height // 2

    # Utiliser textbbox pour obtenir les dimensions du texte
    text_bbox = draw_res.textbbox((0, 0), content.response, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Centrer le texte
    text_x = center_x - text_width // 2
    text_y = center_y - text_height // 2

    draw_res.text((text_x, text_y), content.response, font=font, fill=content.color, align=content.align)
    res.save(f"./upload/{content.language}/Response_{content.language}.jpg")


chat_response = client.chat.complete(
    model= model,
    messages = [
        {
          "role": "user",
          "content": """Créer un jeu 'Qui suis-je?' sur un sportif avec 5 indices numérotés en français,en anglais et en alemand. La réponse en JSON avec ce format
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
  content_data = ContentData(clue_text=content["francais"], position=(500,800), font_size=70 , color=(0,0,0), align="center", fonts="./fonts/Sans.ttf",language="fr",clue_number=content["numero"],response=response_data.name)
  create_template_clues(content_data)



