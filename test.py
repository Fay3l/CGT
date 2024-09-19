import os
# import json 
# from pathlib import Path
# chemin = Path('./upload')

#     # utilisez la méthode is_dir() pour vérifier si chaque élément dans le dossier est un dossier
#     # utilisez la méthode iterdir() pour parcourir tous les éléments dans le dossier
#     # utilisez la fonction sum() pour compter le nombre de dossiers
# noms_de_dossiers = [element.name for element in chemin.iterdir() if element.is_dir()]

# # affichez la liste des noms de dossiers
# for i, nom in enumerate(noms_de_dossiers, start=1):
#     print(f"{i}: {nom}")

# data = """
# {
#     "reponse": 
#         {
#             "french":"L",
#             "english":"E",
#             "german":"O"
#         },
#     "clues":[
#         {
#             "number": 1,
#             "french": "",
#             "english": "",
#             "german": ""
#         },
#         {
#             "number": 2,
#             "french": "",
#             "english": "",
#             "german": ""
#         }
#     ]
# }"""
# json_loads = json.loads(data)

# print("reponse:",json_loads['reponse']['french'])
# from minio import Minio
# # 212.227.131.109:9000
# # 100.96.211.39:9000
# print(os.getenv("MINIO_ACCESS_KEY"))
# client = Minio(endpoint="minio-ts.tail8c4493.ts.net",
#     access_key=os.getenv("MINIO_ACCESS_KEY"),
#     secret_key=os.getenv("MINIO_SECRET_KEY"),
#     secure=True
# )

# # if client.bucket_exists("mybucket"):
# #     print("my-bucket exists")
# # else:
# #     print("my-bucket does not exist")

# objects = client.list_objects("mybucket")
# for obj in objects:
#     print(obj.object_name)

# url = client.presigned_get_object("mybucket", "téléchargement.png")
# print(url)

from pathlib import Path

# Chemin de base où se trouvent les dossiers
chemin = Path('./upload')

# Liste des noms de dossiers
noms_de_dossiers = [element.name for element in chemin.iterdir() if element.is_dir()]

# Listes pour stocker les chemins des fichiers trouvés
fichiers_theme = []
fichiers_clue = []
fichiers_response = []

# Fonction récursive pour rechercher les fichiers dont le nom commence par "theme", "Clue" ou "Response"
def rechercher_fichiers(dossier):
    for element in dossier.iterdir():
        if element.is_dir():
            # Si c'est un dossier, appeler récursivement la fonction
            print(element.name)
            rechercher_fichiers(element)
        elif element.name.startswith('theme'):
            fichiers_theme.append(element)
        elif element.name.startswith('Clue'):
            fichiers_clue.append(element)
        elif element.name.startswith('Response'):
            fichiers_response.append(element)

# Appeler la fonction récursive sur le chemin de base
rechercher_fichiers(chemin)

# Afficher les chemins des fichiers trouvés
print("Fichiers commençant par 'theme':")
for fichier in fichiers_theme:
    print(fichier)
print(fichiers_theme)

print("\nFichiers commençant par 'Clue':")
for fichier in fichiers_clue:
    print(fichier)
print(fichiers_clue)

print("\nFichiers commençant par 'Response':")
for fichier in fichiers_response:
    if "de" in fichier.__str__():
        print(fichier)
print(fichiers_response)

print("\nNoms des dossiers:")
print(noms_de_dossiers)