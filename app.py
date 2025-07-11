import json
import time
from flask import Flask, request, redirect, render_template
import requests
import os
import hashlib
import random
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
# from api import new_templates
from api import new_templates
from classes import State
from minio import Minio, S3Error
from flask_apscheduler import APScheduler
from flask_basicauth import BasicAuth
import logging
class Config:
    SCHEDULER_API_ENABLED = True
    


client = Minio(endpoint="minio-ts.tail8c4493.ts.net",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=True
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config.from_object(Config())
app.config['BASIC_AUTH_USERNAME'] = os.getenv('USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('PASSWORD')
app.secret_key = os.urandom(24)
CORS(app)
basic_auth = BasicAuth(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
state_code = State('','')
CLIENT_KEY = os.getenv('CLIENT_KEY')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = f"{os.getenv('URL')}/callback/"
AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
CONFIG_FILE = os.getenv('CONFIG_FILE')
URL_PREFIX = os.getenv("URL_PREFIX")
PASSWORD =os.getenv("PASSWORD")
UPLOAD_URL = f'{os.getenv("URL")}/upload'

def send_request():
    try:
        create_response = requests.get(os.getenv('URL') + '/create',timeout=None,auth=(os.getenv('USERNAME'),os.getenv('PASSWORD')))
        if create_response.status_code == 200:
            url = f"{os.getenv('URL')}/upload"
            response = requests.get(url,timeout=None)
            if response.status_code == 200:
                print("Requête réussie")
            else:
                print(f"Erreur lors de la requête: {response.text} {response.status_code} ")
                remove_response = requests.get(os.getenv('URL')+'/delete/templates',timeout=None)
                if remove_response.status_code == 200:
                    print("Templates supprimés")
                else:
                    print(f"Erreur lors de la suppression des templates: {remove_response.text} {remove_response}")
    except Exception as e:
        print(f"Exception lors de la fonction send_request(): {e} ")


# Configuration du job pour qu'il s'exécute tous les jours à une heure spécifique
scheduler.add_job(id='send_request_job', func=send_request, trigger='cron', day_of_week='mon-sun', hour=9, minute=0,max_instances=1)
    
def generate_random_string(length):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~' 
    return ''.join(random.choice(characters) for _ in range(length))

def generate_code_verifier():
    return generate_random_string(128)

def generate_code_challenge(code_verifier):
    sha256 = hashlib.sha256(code_verifier.encode()).hexdigest()
    return sha256

def rechercher_fichiers(dossier,list_theme,list_clue,list_response):
    for element in dossier.iterdir():
        if element.is_dir():
            # Si c'est un dossier, appeler récursivement la fonction
            print(element.name)
            rechercher_fichiers(element,list_theme,list_clue,list_response)
        elif element.name.startswith('theme'):
            list_theme.append(element)
        elif element.name.startswith('Clue'):
            list_clue.append(element)
        elif element.name.startswith('Response'):
            list_response.append(element)

def supprimer_fichiers(list_fichiers):
    for fichier in list_fichiers:
        try:
            fichier.unlink()
            print(f"Supprimé : {fichier}")
        except Exception as e:
            print(f"Erreur lors de la suppression de {fichier} : {e}")

@app.route('/')
def hello():
    return '<h1>Api Flask</h1>'

@app.route('/login')
@basic_auth.required
def index():
    return '<a id="login" href="/auth">Login with TikTok</a>'

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/create')
@basic_auth.required
def create():
    try:
        new_templates()
        return 'Success',200
    except Exception as e:
        return f"Error {e}", 401

@app.route('/auth')
def login():
    code_verifier = generate_code_verifier()
    state_code.code_verifier = code_verifier
    code_challenge = generate_code_challenge(code_verifier)
    csrf_state = generate_random_string(30)
    state_code.csrf_state = csrf_state
    # Desktop mode &code_challenge={code_challenge}&code_challenge_method=S256
    auth_url = f'{AUTH_URL}?client_key={CLIENT_KEY}&scope=user.info.basic,video.upload,video.publish&response_type=code&redirect_uri={REDIRECT_URI}&state={csrf_state}&code_challenge={code_challenge}&code_challenge_method=S256'
    return redirect(auth_url)

@app.route('/callback/')
def callback():
    code = request.args.get('code')
    print('code:',code)
    state = request.args.get('state')
    if not state_code.csrf_state:
        return 'CSRF state not found', 500
    if state_code.csrf_state != state:
        return 'CSRF attack detected', 403

    if not state_code.code_verifier:
        return 'Code verifier not found', 400

    token_response = requests.post(TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Cache-Control": "no-cache",
                 "Accept":"application/json"}, 
        data={
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code_verifier": state_code.code_verifier
    })
    print(token_response.url)
    if token_response.status_code == 200:
        token_data = token_response.json()
        print("reponse:",token_response.json())
        try :
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)

            # Mettre à jour les valeurs dans le fichier config.json
            config['access_token'] = token_data.get('access_token', '')
            config['expires_in'] = token_data.get('expires_in', 0)
            config['open_id'] = token_data.get('open_id', '')
            config['refresh_expires_in'] = token_data.get('refresh_expires_in', 0)
            config['refresh_token'] = token_data.get('refresh_token', '')
            config['scope'] = token_data.get('scope', '')
            config['token_type'] = token_data.get('token_type', '')

            # Écrire les nouvelles valeurs dans le fichier config.json
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
                
            return "token obtained",200
        except:
            return token_response.text,500
    else:
        return f'Failed to obtain access token: {token_response.text, token_response.url}', 500
    
@app.route('/upload')
def upload():
    try:
        # spécifiez le chemin du dossier à parcourir
        chemin = Path('./upload')
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
        token = config['access_token']
        print("Token:",token)
        # utilisez la méthode is_dir() pour vérifier si chaque élément dans le dossier est un dossier
        # utilisez la méthode iterdir() pour parcourir tous les éléments dans le dossier
        # utilisez la fonction sum() pour compter le nombre de dossiers
        noms_de_dossiers = [element.name for element in chemin.iterdir() if element.is_dir()]
        fichiers_theme = []
        fichiers_clue = []
        fichiers_response = []
        rechercher_fichiers(chemin,fichiers_theme,fichiers_clue,fichiers_response)
        # affichez la liste des noms de dossiers
        for i, nom in enumerate(noms_de_dossiers, start=1):
            logging.info(f"{i}: {nom}")
            if(nom == "fr"):
                for fichier in fichiers_theme:
                    if "fr" in fichier.__str__():
                        photos_data = [
                            f"{URL_PREFIX}upload/fr/introfr.jpg",
                            f"{URL_PREFIX}upload/fr/butfr.jpg",
                            f"{URL_PREFIX}{fichier}",
                            f"{URL_PREFIX}upload/fr/Clue_1_fr.jpg",
                            f"{URL_PREFIX}upload/fr/Clue_2_fr.jpg",
                            f"{URL_PREFIX}upload/fr/Clue_3_fr.jpg",
                            f"{URL_PREFIX}upload/fr/Clue_4_fr.jpg",
                            f"{URL_PREFIX}upload/fr/Clue_5_fr.jpg",
                            f"{URL_PREFIX}upload/fr/9.jpg",
                            f"{URL_PREFIX}upload/fr/Response_fr.jpg"
                        ]
            if(nom == "en"):
                for fichier in fichiers_theme:
                    if "en" in fichier.__str__():
                        photos_data = [
                            f"{URL_PREFIX}upload/en/introen.jpg",
                            f"{URL_PREFIX}upload/en/buten.jpg",
                            f"{URL_PREFIX}{fichier}",
                            f"{URL_PREFIX}upload/en/Clue_1_en.jpg",
                            f"{URL_PREFIX}upload/en/Clue_2_en.jpg",
                            f"{URL_PREFIX}upload/en/Clue_3_en.jpg",
                            f"{URL_PREFIX}upload/en/Clue_4_en.jpg",
                            f"{URL_PREFIX}upload/en/Clue_5_en.jpg",
                            f"{URL_PREFIX}upload/en/9.jpg",
                            f"{URL_PREFIX}upload/en/Response_en.jpg"
                        ]
            if(nom == "de"):
                for fichier in fichiers_theme:
                    if "de" in fichier.__str__():
                        photos_data = [
                            f"{URL_PREFIX}upload/de/introde.jpg",
                            f"{URL_PREFIX}upload/de/butde.jpg",
                            f"{URL_PREFIX}{fichier}",
                            f"{URL_PREFIX}upload/de/Clue_1_de.jpg",
                            f"{URL_PREFIX}upload/de/Clue_2_de.jpg",
                            f"{URL_PREFIX}upload/de/Clue_3_de.jpg",
                            f"{URL_PREFIX}upload/de/Clue_4_de.jpg",
                            f"{URL_PREFIX}upload/de/Clue_5_de.jpg",
                            f"{URL_PREFIX}upload/de/9.jpg",
                            f"{URL_PREFIX}upload/de/Response_de.jpg"
                        ]
            # URL de l'API TikTok
            url = 'https://open.tiktokapis.com/v2/post/publish/content/init/'

            # En-têtes de la requête
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Données de la requête
            data = {
                "post_info": {
                    "title": "Guessing Game",
                    "description": f" Guessing game Guess the identity of a famous person or fictional character with 5 given clues. #game #guessing #fyp #{nom}",
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "photo_cover_index": 0,
                    "photo_images": photos_data
                },
                "post_mode": "MEDIA_UPLOAD",
                "media_type": "PHOTO"
            }

            # Convertir les données en JSON
            json_data = json.dumps(data)
            print(photos_data)
            # Effectuer la requête POST
            response = requests.post(url, headers=headers, data=json_data)

            if response.status_code == 200:
                response_data = response.json()
                get_data = response_data['data']
                print(get_data)
                publish_id = get_data['publish_id']
                logging.info(publish_id)
                print(response_data)
                
                # Vérifier l'état de l'upload
                status_url = 'https://open.tiktokapis.com/v2/post/publish/status/fetch/'
                
                status_data = {
                    "publish_id": publish_id
                }
                status_json_data = json.dumps(status_data)
                print(f'status xxxxx data ----- {status_data} ')
                while True:
                    status_response = requests.post(status_url, headers=headers, data=status_json_data)
                    status_response_data = status_response.json()
                    print(status_response_data)
                    status = status_response_data['data']['status']
                    logging.info(status)
                    if status == 'PUBLISH_COMPLETE':
                        logging.info("Upload completed successfully.")
                        break
                    elif status == 'SEND_TO_USER_INBOX':
                        logging.info("Upload send user inbox.")
                        break
                    elif status == 'FAILED':
                        logging.info("Upload failed.")
                        return "Upload failed.", 500
                    else:
                        logging.info("Upload in progress. Waiting...")
                        time.sleep(5)  # Attendre 60 secondes avant de vérifier à nouveau
            else:
                return response.text,response.status_code

        # Vérifiez la réponse
        
        # Lister les objets dans le dossier
        objects_de = client.list_objects(os.getenv('MINIO_BUCKET'), prefix="upload/de/",recursive=True)
        objects_en = client.list_objects(os.getenv('MINIO_BUCKET'), prefix="upload/en/",recursive=True)
        objects_fr = client.list_objects(os.getenv('MINIO_BUCKET'), prefix="upload/fr/",recursive=True)
        for obj in objects_de:
            # Supprimer chaque objet
            print("Object:",obj)
            client.remove_object(os.getenv('MINIO_BUCKET'), obj.object_name)
        time.sleep(2)
        for obj in objects_en:
            # Supprimer chaque objet
            client.remove_object(os.getenv('MINIO_BUCKET'), obj.object_name)
        time.sleep(2)
        for obj in objects_fr:
            # Supprimer chaque objet
            client.remove_object(os.getenv('MINIO_BUCKET'), obj.object_name)
        time.sleep(2)
        for theme in fichiers_theme:
            client.remove_object(os.getenv('MINIO_BUCKET'), theme.__str__())
        time.sleep(2)
        print(f"Le dossier upload a été supprimé avec succès.")
        supprimer_fichiers(fichiers_clue)
        supprimer_fichiers(fichiers_response)
        supprimer_fichiers(fichiers_theme)
        return 'Uploaded Successfully', 200
    except Exception as e :
        return f'Except Upload Error {e}', 500

# URL Prefix à vérifier

# Endpoint pour initialiser le téléchargement
@app.route('/videos/user/<path:filename>', methods=['GET'])
def init_download(filename):
    try:
        # Upload the file to S3
        print("File: ",filename)
        client.fput_object(os.getenv('MINIO_BUCKET'),filename,filename)
        url = client.presigned_get_object("mybucket", filename)
        return redirect(url)
    except S3Error as e:
        return f'Error upload_object {e}', 500
    
@app.route('/delete/templates')
def remove():
    try:
        chemin = Path('./upload')
        fichiers_theme = []
        fichiers_clue = []
        fichiers_response = []
        rechercher_fichiers(chemin,fichiers_theme,fichiers_clue,fichiers_response)
        # Lister les objets dans le dossier
        objects_de = client.list_objects(os.getenv('MINIO_BUCKET'), prefix="upload/de/",recursive=True)
        objects_en = client.list_objects(os.getenv('MINIO_BUCKET'), prefix="upload/en/",recursive=True)
        objects_fr = client.list_objects(os.getenv('MINIO_BUCKET'), prefix="upload/fr/",recursive=True)
        for obj in objects_de:
            # Supprimer chaque objet
            print("Object:",obj)
            client.remove_object(os.getenv('MINIO_BUCKET'), obj.object_name)
        time.sleep(2)
        for obj in objects_en:
            # Supprimer chaque objet
            client.remove_object(os.getenv('MINIO_BUCKET'), obj.object_name)
        time.sleep(2)
        for obj in objects_fr:
            # Supprimer chaque objet
            client.remove_object(os.getenv('MINIO_BUCKET'), obj.object_name)
        time.sleep(2)
        for theme in fichiers_theme:
            client.remove_object(os.getenv('MINIO_BUCKET'), theme.__str__())
        time.sleep(2)
        print(f"Le dossier upload a été supprimé avec succès.")
        supprimer_fichiers(fichiers_clue)
        supprimer_fichiers(fichiers_response)
        supprimer_fichiers(fichiers_theme)
        return 'Success',200
    except Exception as e:
        return f'Error remove {e}',500

@app.route("/cuty")
def url():
    return '<p><a href="https://cuty.io/kPW3w2">Link</a></p><a href="https://cuty.io/lMWhCQ">Link2</a>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=False)
        