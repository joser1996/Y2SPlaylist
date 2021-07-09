from flask import Flask, redirect, request
from dotenv import load_dotenv
from pathlib import Path
import requests
import urllib
import os
import pickle

dotenv_path = Path('../.env')
authAppEndpoint = 'https://accounts.spotify.com/authorize?'
load_dotenv(dotenv_path=dotenv_path)
app = Flask(__name__)
@app.route('/')
def hello():
	print('Hello World')
	return 'Hello World'

@app.route('/request-auth', methods = ['GET'])
def requestAuthorization():
	print('In requestAuthorization')
	getVars = {
		'client_id': os.environ.get('SPOTIFY_CLIENT_ID'),
		'response_type': 'code',
		'redirect_uri': os.environ.get('SPOTIFY_URI'),
		'scope': 'playlist-read-private playlist-modify-private'
	}
	url = authAppEndpoint + urllib.parse.urlencode(getVars)
	print("URL: ", url)
	return redirect(url)

@app.route('/callback')
def callbackRoute():
	print("In callbackRoute")
	code = request.args.get('code')
	#print("Code: ", code)
	# Might need to save auth code?
	requestTokens(code)
	return('Done!')


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



#Route to handle 

if __name__== '__main__':
	app.run(debug=True, host="localhost", port=8888)
