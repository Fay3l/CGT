from dataclasses import dataclass
from typing import Tuple,List
from PIL import Image, ImageDraw, ImageFont


@dataclass
class Response:
    clues:str
    language:str
    person:str
    theme:str
    name:str

@dataclass
class TextData:
    content: str
    position: Tuple[int, int]  # (x, y) position
    font_size: int
    color: Tuple[int, int, int]  # (R, G, B) color
    align: str 
    fonts: str

def create_instagram_story(texts: List[TextData], output_path: str):
    # Créer une image vierge
    image = Image.new('RGB', (1080, 1920), color=(217, 217, 217))

    draw = ImageDraw.Draw(image)

    # Ajouter les textes à l'image
    for text in texts:
        try:
            font = ImageFont.truetype(font = text.fonts, size=text.font_size)
        except IOError:
            font = ImageFont.load_default()
            print(IOError)
        draw.text(text.position, text.content, font=font, fill=text.color,align=text.align)

    # Enregistrer l'image
    image.save(output_path)

# Exemple d'utilisation
res = Response(name="Jeu de devinette",clues="",language="fr",person="",theme="Sport")

texts = [
    TextData(content=res.name, position=(200, 960), font_size=90, color=(0, 0, 0),align="center",fonts="./fonts/Sans.ttf"),
]

create_instagram_story(texts, "instagram_story.png")