from dataclasses import dataclass
from typing import Tuple,List,Optional
from PIL import Image, ImageDraw, ImageFont

@dataclass
class Clues:
    numero:int
    français:str
    anglais:str
    allemand:str

@dataclass
class Response:
    clues:List[Clues]
    name:str

@dataclass
class ImageData:
    path: str
    image:Optional[str]
    
@dataclass
class ContentData:
    clue_text: str
    image:Optional[str]
    position: Tuple[int, int]  # (x, y) position
    font_size: int
    color: Tuple[int, int, int]  # (R, G, B) color
    align: str 
    fonts: str
    language:Optional[str]
    clue_number:Optional[int]

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
    



content=[ContentData(clue_text="Jeu\n\nde\n\ndevinettes",language="fr", position=(210, 800),image="",clue_number=0, font_size=140, color=(0, 0, 0),align="center",fonts="./fonts/Sans.ttf"),
        ContentData(clue_text="Qui suis-je ?",language="fr", position=(300, 1600),image="",clue_number=0 ,font_size=80, color=(0, 0, 0),align="center",fonts="./fonts/Sans.ttf"),]

# create_instagram_story(images)
open_instagram_story(content)