from dataclasses import dataclass
from typing import Tuple,List,Optional


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







