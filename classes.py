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
    response:str

@dataclass
class TemplateData:
    content:List[ContentData]
    path:str

@dataclass
class Theme:
    name:str

@dataclass
class State:
    csrf_state:Optional[str]
    code_verifier:Optional[str]

@dataclass
class Token:
    access_token: Optional[str]
    expires_in: Optional[str]
    open_id: Optional[str]
    refresh_expires_in: Optional[str]
    refresh_token: Optional[str]
    scope: Optional[str]
    token_type: Optional[str]



