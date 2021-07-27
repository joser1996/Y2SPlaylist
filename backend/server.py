from flask import Flask, redirect, request
from dotenv import load_dotenv
from pathlib import Path
import requests
import urllib
import os
import pickle
import time

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)


app = Flask(__name__)
@app.route('/')
def hello():
	print('Hello World')
	return 'Hello World'

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
	app.run(debug=True, host="localhost", port=8888)
