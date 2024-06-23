from flask import Flask, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

google_client_id = 'your_google_client_id_here'
google_client_secret = 'your_google_client_secret_here'
google_redirect_uri = 'http://localhost:5000/authorize'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=google_client_id,
    client_secret=google_client_secret,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=google_redirect_uri,
    client_kwargs={'scope': 'email profile'},
)

@app.route('/')
def index():
    if 'google_token' in session:
        token = session['google_token']
        resp = google.get('userinfo', token=token)
        return jsonify(resp.json())
    return 'Hello! Log in with your Google account: <a href="/login">Log in</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    session['google_token'] = token
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
