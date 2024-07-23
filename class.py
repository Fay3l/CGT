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
    text: str
    position: Tuple[int, int]  # (x, y) position
    font_size: int
    color: Tuple[int, int, int]  # (R, G, B) color
    align: str 
    fonts: str

@dataclass
class ImageData:
    content:List[TextData]
    path:str



def create_instagram_story(images: List[ImageData]):
    # Créer les images vierges
    for image in images:
        new_image = Image.new('RGB', (1080, 1920), color=(217, 217, 217))
        draw = ImageDraw.Draw(new_image)
        # Ajouter les textes à l'image
        for text in image.content:
            try:
                font = ImageFont.truetype(font = text.fonts, size=text.font_size)
            except IOError:
                font = ImageFont.load_default()
                print(IOError)
            draw.text(text.position, text.text, font=font, fill=text.color,align=text.align)
    # Enregistrer l'image
        new_image.save(image.path)

# Exemple d'utilisation
res = Response(name="Jeu\n\n de\n\n devinette",clues="",language="fr",person="",theme="Sport")
res1 = Response(name="Qui suis-je ?",clues="",language="fr",person="",theme="Sport")

images = [
    ImageData(path="story.png",content=[TextData(text=res.name, position=(300, 960), font_size=100, color=(0, 0, 0),align="center",fonts="./fonts/Sans.ttf"),
                                        TextData(text=res1.name, position=(300, 980), font_size=100, color=(0, 0, 0),align="center",fonts="./fonts/Sans.ttf")])

]

create_instagram_story(images)