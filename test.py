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

def find_files_starting_with(directory, prefix):
    # Liste pour stocker les chemins des fichiers trouvés
    matching_files = []

    # Parcourir le répertoire et ses sous-répertoires
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith(prefix):
                # Ajouter le chemin complet du fichier à la liste
                matching_files.append(os.path.join(root, file))

    return matching_files

# Exemple d'utilisation
directory_to_search = '/upload/en'
prefix = 'theme'

files = find_files_starting_with(directory_to_search, prefix)

# Afficher les fichiers trouvés
for file in files:
    print(file)