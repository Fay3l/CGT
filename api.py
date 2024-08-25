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

def get_text_width(text, font):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]

def justify_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width = get_text_width(word, font)
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + get_text_width(' ', font)
        else:
            lines.append(current_line)
            current_line = [word]
            current_width = word_width + get_text_width(' ', font)

    if current_line:
        lines.append(current_line)

    justified_lines = []
    for line in lines:
        if len(line) == 1:
            justified_lines.append(' '.join(line))
        else:
            total_width = sum(get_text_width(word, font) for word in line) + get_text_width(' ', font) * (len(line) - 1)
            extra_space = (max_width - total_width) // (len(line) - 1)
            justified_line = line[0]
            for word in line[1:]:
                justified_line += ' ' * (extra_space // get_text_width(' ', font)) + ' ' + word
            justified_lines.append(justified_line)

    return '\n'.join(justified_lines)

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
      template.save(f"Clue_{content.clue_number}_{content.language}.jpg")

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
  content_data = ContentData(clue_text=content["francais"], position=(500,800), font_size=70 , color=(0,0,0), align="center", fonts="./fonts/Sans.ttf",language="fr",clue_number=content["numero"])
  create_template_clues(content_data)


# def create_instagram_story(template: List[TemplateData]):
#     # Créer les images vierges
#     for image in template:
#         new_image = Image.new('RGB', (1080, 1920), color=(217, 217, 217))
#         draw = ImageDraw.Draw(new_image)
#         # Ajouter les textes à l'image
#         for text in image.content:
#             try:
#                 if(text.image):
#                     foreground_image = Image.open(text.image)
#                     foreground_image = foreground_image.resize((150, 150))  # Redimensionner si nécessaire    
#                     position = (300, 200)
#                 font = ImageFont.truetype(font = text.fonts, size=text.font_size)
#             except IOError:
#                 font = ImageFont.load_default()
#                 print(IOError)
#             draw.text(text.position, text.clue_text, font=font, fill=text.color,align=text.align)
#     # Enregistrer l'image
#         new_image.save(image.path)


    


