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
class ImageData:
    path: str
    image:str | None
    
@dataclass
class ContentData:
    text: str
    image:str | None
    position: Tuple[int, int]  # (x, y) position
    font_size: int
    color: Tuple[int, int, int]  # (R, G, B) color
    align: str 
    fonts: str
    language:str

@dataclass
class TemplateData:
    content:List[ContentData]
    path:str



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
            draw.text(text.position, text.text, font=font, fill=text.color,align=text.align)
    # Enregistrer l'image
        new_image.save(image.path)

def open_instagram_story(content: List[ContentData]):
    # Créer les images vierges
        # Ajouter les textes à l'image
    for count,data in enumerate(content):
        match
        
        try:
            font = ImageFont.truetype(font = data.fonts, size=data.font_size)
        except IOError:
            font = ImageFont.load_default()
            print(IOError)
        draw.text(data.position, data.text, font=font, fill=data.color,align=data.align)
# Enregistrer l'image
    new_image.save(image.path)

# Exemple d'utilisation
res = Response(name="Jeu\n\n de\n\n devinette",clues="",language="fr",person="",theme="Sport")
res1 = Response(name="Qui suis-je ?",clues="",language="fr",person="",theme="Sport")

images = [
    TemplateData(path="français.png",content=[ContentData(text="Jeu\n\nde\n\ndevinettes", position=(210, 800), font_size=140, color=(0, 0, 0),align="center",fonts="./fonts/Sans.ttf"),
                                        ContentData(text="Qui suis-je ?", position=(300, 1600), font_size=80, color=(0, 0, 0),align="center",fonts="./fonts/Sans.ttf"),
                                        ContentData(text="",image="./images/drapeau_fr.png")])

]
content=[ContentData(text="Jeu\n\nde\n\ndevinettes", position=(210, 800), font_size=140, color=(0, 0, 0),align="center",fonts="./fonts/Sans.ttf"),
                                        ContentData(text="Qui suis-je ?", position=(300, 1600), font_size=80, color=(0, 0, 0),align="center",fonts="./fonts/Sans.ttf"),
                                        ContentData(text="",image="./images/drapeau_fr.png")]

create_instagram_story(images)