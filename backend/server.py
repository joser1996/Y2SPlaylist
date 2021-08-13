from flask import Flask, redirect, request, session
from dotenv import load_dotenv
from pathlib import Path
from requests_oauthlib import OAuth2Session
import requests
import urllib
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
import pickle
import time

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)


app = Flask(__name__)
@app.route('/')
def hello():
	print('Hello World')
	return 'Hello World'


@app.route('/auth/google', methods = ['GET'])
def googleRequestAuth():
	auth_url = "https://accounts.google.com/o/oauth2/v2/auth"

	scope = [
	"https://www.googleapis.com/auth/youtube.force-ssl",
	"https://www.googleapis.com/auth/youtube.upload"
	]
	google = OAuth2Session(os.environ.get('GOOGLE_CLIENT_ID'), scope=scope, redirect_uri=os.environ.get('GOOGLE_URI'))

	authorization_url, state = google.authorization_url(auth_url,
	#offline for refresh token
	#force user to always click to authorize
	access_type="offline", prompt="select_account")
	#State is used to prevent CSRF
	session['oauth_state'] = state
	#should redirect us to log in
	return redirect(authorization_url)


@app.route('/google/auth/callback')
def googleCallback():
	token_url = "https://www.googleapis.com/oauth2/v4/token"
	google = OAuth2Session(os.environ.get('GOOGLE_CLIENT_ID'), state=session['oauth_state'])
	token = google.fetch_token(token_url,
		client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
		authorization_response=request.url
	)
	print("Got token: ", token)
	yt = YouTubeClient("", token)
	ls = yt.getPlaylists()
	print("Playlists: ", ls)
	return ls;


@app.route('/request-auth', methods = ['GET'])
def requestAuthorization():
	authAppEndpoint = 'https://accounts.spotify.com/authorize?'
	getVars = {
		'client_id': os.environ.get('SPOTIFY_CLIENT_ID'),
		'response_type': 'code',
		'redirect_uri': os.environ.get('SPOTIFY_URI'),
		'scope': 'playlist-read-private playlist-modify-private playlist-modify-public'
	}
	url = authAppEndpoint + urllib.parse.urlencode(getVars)
	return redirect(url)

@app.route('/callback')
def callbackRoute():
	print("In callbackRoute")
	code = request.args.get('code')
	requestTokens(code)
	return('Done! You may close the window')


@app.route('/refresh-tokens')
def refreshTokens():
	tokens_url = "https://accounts.spotify.com/api/token"
	try:
		tokens = pickle.load(open("tokens.pkl", "rb"))
		refresh_token = tokens['refresh_token']
		payload = {
			'grant_type': 'refresh_token',
			'refresh_token': refresh_token
		}
		header = {
			'Authorization': 'application/x-www-form-urlencoded'
		}
		response = requests.post(
			tokens_url,
			auth=(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET')),
			data=payload,
			headers=header
		)
		obj = res.json()
		new_token = response.get('access_token')
		new_time = {
			'origin': round(time.time())
		}
		fp = open('origin_time.pkl', 'wb')
		pickle.dump(new_time, fp)
		fp.close()
		new_token = {
			'access_token': new_token,
			'refresh_token': refresh_token
		}
		fp = open('tokens.pkl', 'wb')
		pickle.dump(new_token, fp)
		fp.close()
	except:
		print("Couldn't refresh tokens!!")

def requestTokens(auth_code):
	print("In requestTokens")
	url = 'https://accounts.spotify.com/api/token'
	body = {
		'grant_type': 'authorization_code',
		'code': auth_code,
		'redirect_uri': os.environ.get('SPOTIFY_URI')
	}
	response = requests.post(
		url,
		auth=(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET')),
		data=body
	)
	# Assuming all goes well get tokens from here
	obj = response.json()
	fp = open("tokens.pkl", "wb")
	tokens = {
		"access_token": obj['access_token'],
		"refresh_token": obj['refresh_token']
	}
	pickle.dump(tokens, fp)
	fp.close()
	current_time = round(time.time())
	fp = open("origin.pkl", "wb")
	o_time = {
		"origin_time": current_time
	}
	pickle.dump(o_time, fp)
	fp.close()



#Route to handle 

if __name__== '__main__':
	app.secret_key = 'super duper secret key'
	app.run(debug=True, host="localhost", port=8888)
