import json
from flask import Flask, jsonify, request, redirect, render_template
import requests
import os
import hashlib
import logging
import random
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
from classes import State
from minio import Minio, S3Error
client = Minio(endpoint="minio-ts.tail8c4493.ts.net",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=True
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)
state_code = State('','')
CLIENT_KEY = os.getenv('CLIENT_KEY')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:5000/callback/"
AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
CONFIG_FILE = os.getenv('CONFIG_FILE')
URL_PREFIX = "https://fay.tail8c4493.ts.net/videos/user/"



def generate_random_string(length):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~'
    return ''.join(random.choice(characters) for _ in range(length))

def generate_code_verifier():
    return generate_random_string(128)

def generate_code_challenge(code_verifier):
    sha256 = hashlib.sha256(code_verifier.encode()).hexdigest()
    return sha256

@app.route('/')
def index():
    return '<a href="/auth">Login with TikTok</a>'

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/auth')
def login():
    code_verifier = generate_code_verifier()
    state_code.code_verifier = code_verifier
    code_challenge = generate_code_challenge(code_verifier)
    csrf_state = generate_random_string(30)
    state_code.csrf_state = csrf_state
    auth_url = f'{AUTH_URL}?client_key={CLIENT_KEY}&scope=user.info.basic,video.publish&response_type=code&redirect_uri={REDIRECT_URI}&state={csrf_state}&code_challenge={code_challenge}&code_challenge_method=S256'
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
                
            return token_data,200
        except:
            return token_response.text,500
    else:
        return f'Failed to obtain access token: {token_response.text, token_response.url}', 500
    
@app.route('/upload')
def upload():
    
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
    # affichez la liste des noms de dossiers
    for i, nom in enumerate(noms_de_dossiers, start=1):
        print(f"{i}: {nom}")
        if(nom == "fr"):
            photos_data = [
                "https://fay.tail8c4493.ts.net/videos/user/upload/fr/introfr.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/fr/butfr.jpg",
                # "https://fay.tail8c4493.ts.net/videos/user/upload/fr/theme_sport_fr.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/fr/Clue_1_fr.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/fr/Clue_2_fr.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/fr/Clue_3_fr.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/fr/Clue_4_fr.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/fr/Clue_5_fr.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/fr/9.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/fr/Response_fr.jpg"
            ]
        if(nom == "en"):
            photos_data = [
                "https://fay.tail8c4493.ts.net/videos/user/upload/en/introen.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/en/buten.jpg",
                # "https://fay.tail8c4493.ts.net/videos/user/upload/en/theme_sport_en.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/en/Clue_1_en.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/en/Clue_2_en.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/en/Clue_3_en.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/en/Clue_4_en.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/en/Clue_5_en.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/en/9.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/en/Response_en.jpg"
            ]
        if(nom == "de"):
            photos_data = [
                "https://fay.tail8c4493.ts.net/videos/user/upload/de/introde.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/de/butde.jpg",
                # "https://fay.tail8c4493.ts.net/videos/user/upload/de/theme_sport_de.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/de/Clue_1_de.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/de/Clue_2_de.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/de/Clue_3_de.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/de/Clue_4_de.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/de/Clue_5_de.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/de/9.jpg",
                "https://fay.tail8c4493.ts.net/videos/user/upload/de/Response_de.jpg"
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
                "title": "funny cat",
                "description": "this will be a #funny photomode on your @tiktok #fyp",
                "disable_comment": True,
                "privacy_level": "SELF_ONLY",
                "auto_add_music": True
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "photo_cover_index": 0,
                "photo_images": photos_data
            },
            "post_mode": "DIRECT_POST",
            "media_type": "PHOTO"
        }

        # Convertir les données en JSON
        json_data = json.dumps(data)

        # Effectuer la requête POST
        response = requests.post(url, headers=headers, data=json_data)

        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
        else:
            return response.text,response.status_code

    # Vérifiez la réponse
    
    return 'Uploaded Successfully', 200
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)