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
    themes = ["un_sportif","une_personne_historique","un_personnage_de_fiction","un_personnage_de_manga","un_scientifique"]
    return Theme(random.choice(themes))

def lire_fichier(nom_fichier):
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()
    return lignes

def choisir_personne(lignes):
    # Supprimer la première ligne qui contient le titre
    # lignes = lignes[1:]
    # Supprimer les lignes vides et les numéros de ligne
    sportifs = [ligne.split('. ')[1].strip() for ligne in lignes if ligne.strip()]
    return random.choice(sportifs)

def create_template_clues(content: ContentData, theme: str):
    # Créer les images vierges
    # Ajouter les textes à l'image
    template = Image.open(f"./template/{content.language}/{content.clue_number}.jpg")
    draw = ImageDraw.Draw(template)

    try:
        font = ImageFont.truetype(font=content.fonts, size=content.font_size)
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
    total_height = sum(line_heights) + len(lines) * 10  # Ajouter un espacement de 10 pixels entre les lignes

    # Calculer la position centrale verticale
    y_start = (box_height - total_height) // 2

    # Ajouter chaque ligne à l'image
    for i, line in enumerate(lines):
        line_width = draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]
        x = (box_width - line_width) // 2
        y = y_start + sum(line_heights[:i]) + i * 10  # Ajouter un espacement de 10 pixels entre les lignes
        draw.text((x, y), line, font=font, fill=content.color)

    template.save(f"./upload/{content.language}/Clue_{content.clue_number}_{content.language}.jpg")

    # Supposons que res est votre image et content.response est votre texte
    res = Image.open(f"./template/{content.language}/10.jpg")
    draw_res = ImageDraw.Draw(res)

    # Diviser le texte de la réponse en mots
    response_words = content.response.split()
    response_lines = []
    current_response_line = []
    box_width, box_height = res.size
    max_width = box_width * 0.9  # Laisser un peu de marge

    for word in response_words:
        test_line = ' '.join(current_response_line + [word])
        line_width, _ = draw_res.textbbox((0, 0), test_line, font=font)[2:4]

        if line_width > max_width:
            response_lines.append(' '.join(current_response_line))
            current_response_line = [word]
        else:
            current_response_line.append(word)

    if current_response_line:
        response_lines.append(' '.join(current_response_line))

    # Calculer la taille de chaque ligne de la réponse
    response_line_heights = [draw_res.textbbox((0, 0), line, font=font)[3] - draw_res.textbbox((0, 0), line, font=font)[1] for line in response_lines]
    total_response_height = sum(response_line_heights) + len(response_lines) * 10  # Ajouter un espacement de 10 pixels entre les lignes

    # Calculer la position centrale verticale pour la réponse
    y_start_response = (box_height - total_response_height) // 2

    # Ajouter chaque ligne de la réponse à l'image
    for i, line in enumerate(response_lines):
        line_width = draw_res.textbbox((0, 0), line, font=font)[2] - draw_res.textbbox((0, 0), line, font=font)[0]
        x = (box_width - line_width) // 2
        y = y_start_response + sum(response_line_heights[:i]) + i * 10  # Ajouter un espacement de 10 pixels entre les lignes
        draw_res.text((x, y), line, font=font, fill=content.color)

    res.save(f"./upload/{content.language}/Response_{content.language}.jpg")

    if "sport" in theme.name:
        theme_sport = Image.open(f"./template/{content.language}/theme_sport_{content.language}.jpg")
        theme_sport.save(f"./upload/{content.language}/theme_sport_{content.language}.jpg")

    if "fiction" in theme.name:
        theme_film = Image.open(f"./template/{content.language}/theme_film_{content.language}.jpg")
        theme_film.save(f"./upload/{content.language}/theme_film_{content.language}.jpg")

    if "hist" in theme.name:
        theme_histoire = Image.open(f"./template/{content.language}/theme_histoire_{content.language}.jpg")
        theme_histoire.save(f"./upload/{content.language}/theme_histoire_{content.language}.jpg")

    if "manga" in theme.name:
        theme_manga = Image.open(f"./template/{content.language}/theme_manga_{content.language}.jpg")
        theme_manga.save(f"./upload/{content.language}/theme_manga_{content.language}.jpg")
    
    if "scien" in theme.name:
        theme_science = Image.open(f"./template/{content.language}/theme_science_{content.language}.jpg")
        theme_science.save(f"./upload/{content.language}/theme_science_{content.language}.jpg")

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
        return False
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
        return True




def new_templates():
    try:
        while True:
            theme_aleatoire = choisir_profession_aleatoire()
            print(f"Theme choisi aléatoirement : {theme_aleatoire.name.replace('_',' ')}")
            match theme_aleatoire:
                case Theme("un_sportif"):
                    nom_fichier = 'list/sportifs.txt'
                    lignes = lire_fichier(nom_fichier)
                    personne_choisi = choisir_personne(lignes)
                case Theme("une_personne_historique"):
                    nom_fichier = 'list/historiques.txt'
                    lignes = lire_fichier(nom_fichier)
                    personne_choisi = choisir_personne(lignes)
                case Theme("un_personnage_de_manga"):
                    nom_fichier = 'list/manga.txt'
                    lignes = lire_fichier(nom_fichier)
                    personne_choisi = choisir_personne(lignes)
                case Theme("un_personnage_de_fiction"):
                    nom_fichier = 'list/film.txt'
                    lignes = lire_fichier(nom_fichier)
                    personne_choisi = choisir_personne(lignes)
                case Theme("un_scientifique"):
                    nom_fichier = 'list/scientifiques.txt'
                    lignes = lire_fichier(nom_fichier)
                    personne_choisi = choisir_personne(lignes)
            print(f"Personnage choisi aléatoirement : {personne_choisi}")
            chat_response = client.chat.complete(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": f"Faire le jeu 'Qui suis-je?' sur {personne_choisi} avec 5 indices en francais, en anglais et en allemand. La réponse du jeu doit avoir son prénom et son nom de famille. Mettre le résultat en JSON avec ce format:" +
                        """{
                            "reponse": {
                            "french":"",
                            "english":"",
                            "german":"",
                            },
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

            response_data = Response(clues=json_loads['clues'], name=json_loads['reponse']['french'])

            if not database(reponse=response_data.name, theme=theme_aleatoire.name):
                print("Break! !")
                return False
            else:
                print("content")
                for content in response_data.clues:
                    print('create !!!')
                    content_data = ContentData(
                        clue_text=content["french"],
                        position=(500, 800),
                        font_size=70,
                        color=(0, 0, 0),
                        align="center",
                        fonts="./fonts/Sans.ttf",
                        language="fr",
                        clue_number=content["number"],
                        response=json_loads['reponse']['french']
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
                        response=json_loads['reponse']['english']
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
                        response=json_loads['reponse']['german']
                    )
                    create_template_clues(content_data, theme_aleatoire)
                return True
    except:
        return False

