from mistralai import Mistral
import os
from dotenv import load_dotenv
import json
from PIL import Image, ImageDraw, ImageFont
from classes import Response, ContentData,Theme
load_dotenv()


api_key = os.getenv("MISTRALAPI_KEY")
client_key = os.getenv("CLIENT_KEY")
client_secret =os.getenv("CLIENT_SECRET")
model = "open-mistral-7b"

client = Mistral(api_key=api_key)
import random



# Fonction pour choisir une valeur aléatoire parmi les membres de l'énumération
def choisir_profession_aleatoire():
    themes = ["un_sportif","un_personnage_historique","une_sportive","un_personnage_de_film","un_personnage_de_manga"]
    return Theme(random.choice(themes))

def create_template_clues(content: ContentData,theme:str):
    # Créer les images vierges
    # Ajouter les textes à l'image
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
    if "sport" in theme.name: 
      theme_sport = Image.open(f"./template/{content.language}/theme_sport_{content.language}.jpg")
      theme_sport.save(f"./upload/{content.language}/theme_sport_{content.language}.jpg")
    if "film" in theme.name: 
      theme_film = Image.open(f"./template/{content.language}/theme_film_{content.language}.jpg")
      theme_film.save(f"./upload/{content.language}/theme_film_{content.language}.jpg")
    if "hist" in theme.name: 
      theme_histoire = Image.open(f"./template/{content.language}/theme_histoire_{content.language}.jpg")
      theme_histoire.save(f"./upload/{content.language}/theme_histoire_{content.language}.jpg")
    if "hist" in theme.name: 
      theme_manga = Image.open(f"./template/{content.language}/theme_manga_{content.language}.jpg")
      theme_manga.save(f"./upload/{content.language}/theme_manga_{content.language}.jpg")

def database(reponse: str, theme: str):
    filename = "data.json"
    data = []
    # Vérifier si le fichier existe et n'est pas vide
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        data = []
    else:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

    print("data", data)

    # Vérifier si la réponse est dans le fichier JSON 
    if any(item.get("reponse") == reponse for item in data):
        print("La réponse est déjà dans le fichier JSON.")
        return True
    else:
        print("La réponse n'est pas dans le fichier JSON.")
        # Écrire les données mises à jour dans le fichier JSON
        if isinstance(data, list):
        # Trouver la valeur maximale de la clé 'id'
          max_id = max(item.get("id", 0) for item in data) if data else 0
          print(f"La valeur maximale de l'id est : {max_id}")
          json_data = {
              "id": max_id + 1,
              "reponse": reponse,
              "theme": theme,
          }
          data.append(json_data)
        else:
            print("Le fichier JSON ne contient pas une liste d'objets.")
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        return False


theme_aleatoire = choisir_profession_aleatoire()
print(f"Theme choisi aléatoirement : {theme_aleatoire.name.replace('_',' ')}")

while True:
    difficulté = ["connu","peu connu","moins connu"]
    difficulté_choisie = random.choice(difficulté)
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Créer un jeu 'Qui suis-je?' sur {theme_aleatoire.name.replace('_',' ')} {difficulté_choisie} avec 5 indices numérotés en francais,en anglais et en allemand. La réponse en JSON avec ce format:" +
                """{
                  "reponse": "",
                  "clues":[
                  {
                    "number": 1,
                    "french": "",
                    "english": "",
                    "german": ""
                  },
                ]
                }
                }""",
            },
        ],
        response_format={
            "type": "json_object",
        }
    )
    response = chat_response.choices[0].message.content
    print(response)
    try:
        json_loads = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Erreur lors de la conversion du JSON: {e}")
        continue

    response_data = Response(clues=json_loads['clues'], name=json_loads['reponse'])

    if not database(reponse=response_data.name, theme=theme_aleatoire.name):
      break

for content in response_data.clues:
  content_data = ContentData(
      clue_text=content["french"],
      position=(500, 800),
      font_size=70,
      color=(0, 0, 0),
      align="center",
      fonts="./fonts/Sans.ttf",
      language="fr",
      clue_number=content["number"],
      response=response_data.name
  )
  create_template_clues(content_data, theme_aleatoire)
  content_data = ContentData(
      clue_text=content["english"],
      position=(500, 800),
      font_size=70,
      color=(0, 0, 0),
      align="center",
      fonts="./fonts/Sans.ttf",
      language="en",
      clue_number=content["number"],
      response=response_data.name
  )
  create_template_clues(content_data, theme_aleatoire)
  content_data = ContentData(
      clue_text=content["german"],
      position=(500, 800),
      font_size=70,
      color=(0, 0, 0),
      align="center",
      fonts="./fonts/Sans.ttf",
      language="de",
      clue_number=content["number"],
      response=response_data.name
  )
  create_template_clues(content_data, theme_aleatoire)


