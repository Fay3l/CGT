from datetime import timedelta
from flask import Flask, request, redirect, render_template
import requests
import os
import hashlib
import logging
import random
from flask_cors import CORS
from dotenv import load_dotenv

from classes import State, Token

load_dotenv()

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)
state_code = State('','')
token = Token('','','','','','','')
CLIENT_KEY = os.getenv('CLIENT_KEY')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:5000/callback/"
AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
CODE_VERIFIER =''
CSRF_STATE=''



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
    print('aaaaaaaaaaaaaaaaaaaaaaaaa',code_verifier)
    print('xxxxxxxxxxxxxxxxxxxxxxxxx',csrf_state)
    state_code.csrf_state = csrf_state
    auth_url = f'{AUTH_URL}?client_key={CLIENT_KEY}&scope=user.info.basic&response_type=code&redirect_uri={REDIRECT_URI}&state={csrf_state}&code_challenge={code_challenge}&code_challenge_method=S256'
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
            if token_data['access_token']:
                token.access_token = token_data['access_token']
                token.refresh_token = token_data['refresh_token']
                token.refresh_expires_in = token_data['refresh_expires_in']
                token.token_type = token_data['token_type']
                token.scope = token_data['scope']
                token.open_id = token_data['open_id']
                
                return token_data,200
        except:
            return token_response.text,500
    else:
        return f'Failed to obtain access token: {token_response.text, token_response.url}', 500
    
@app.route('/upload')
def upload():
    URL = 'https://open.tiktokapis.com/v2/post/publish/content/init/'

    # Préparez les données pour la requête POST
    data = {
        "post_info": {
            "title": "funny cat",
            "description": "this will be a #funny photo on your @tiktok #fyp"
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "photo_cover_index": 1,
            "photo_images": [
                "https://tiktokcdn.com/obj/example-image-01.webp",
                "https://tiktokcdn.com/obj/example-image-02.webp"
            ]
        },
        "post_mode": "MEDIA_UPLOAD",
        "media_type": "PHOTO"
    }

    # Envoyez la requête POST
    response = requests.post(URL,
        headers={
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        },
        data=data
    )

    # Vérifiez la réponse
    if response.status_code == 200:
        response_data = response.json()
        print("Response:", response_data)
    else:
        print()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)