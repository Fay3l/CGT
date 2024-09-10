import os
from pathlib import Path

# spécifiez le chemin du dossier à parcourir
chemin = Path('D:/CGT/upload')

# utilisez la méthode is_dir() pour vérifier si chaque élément dans le dossier est un dossier
# utilisez la méthode iterdir() pour parcourir tous les éléments dans le dossier
# utilisez la fonction sum() pour compter le nombre de dossiers
noms_de_dossiers = [element.name for element in chemin.iterdir() if element.is_dir()]

# affichez la liste des noms de dossiers
for i, nom in enumerate(noms_de_dossiers, start=1):
    print(f"{i}: {nom}")