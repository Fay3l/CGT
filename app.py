from flask import Flask, request, redirect, session, render_template
import requests
import os
import hashlib
import logging
import random
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

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
    session['code_verifier'] = code_verifier
    code_challenge = generate_code_challenge(code_verifier)
    csrf_state = generate_random_string(30)
    session['csrf_state'] = csrf_state
    CSRF_STATE = csrf_state
    auth_url = f'{AUTH_URL}?client_key={CLIENT_KEY}&scope=user.info.basic&response_type=code&redirect_uri={REDIRECT_URI}&state={csrf_state}&code_challenge={code_challenge}&code_challenge_method=S256'
    return redirect(auth_url)

@app.route('/callback/')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    print(CSRF_STATE)
    if not session.get('csrf_state'):
        print("csrf_state not found in session")
        return 'CSRF state not found', 500
    if session.get('csrf_state') != state:
        return 'CSRF attack detected', 403

    if not session['code_verifier']:
        return 'Code verifier not found', 400

    token_response = requests.post(TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"}, 
        data={
        'client_id': CLIENT_KEY,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code_verifier': session['code_verifier']
    })

    if token_response.status_code == 200:
        token_data = token_response.json()
        session['access_token'] = token_data['access_token']
        return 'Logged in successfully!'
    else:
        return f'Failed to obtain access token: {token_response.text, token_response.url}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)