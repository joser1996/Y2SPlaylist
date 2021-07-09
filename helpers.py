import pickle
import time
import requests

def tokenIsFresh():
	fp = open('origin.pkl', 'rb')
	obj = pickle.load(fp)
	origin_time = obj['origin_time']
	current_time = round(time.time())
	delta_time = current_time - origin_time
	ONE_HOUR = 3600
	if (delta_time > ONE_HOUR or current_time < origin_time):
		print("Refreshing Tokens")
		return false
	else:
		print("Token is fresh.")
		return True

def refreshAccessToken():
	url = 'https://accounts.spotify.com/api/token'
	fp = open('tokens.pkl', 'rb')
	tokens = pickle.load(fp)
	fp.close()
	refresh_token = tokens['refresh_token']
	payload = {
		'grant_type': 'refresh_token',
		'refresh_token': refresh_token
	}
	header = {
		'Authorization': 'application/x-www-form-urlencoded'
	}
	response = requests.post(
		url,
		auth=(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET')),
		data=payload,
		headers=header
	)
	response_data = response.json()
	tokens = {
		'access_token': response_data['access_token'],
		'refresh_token': refresh_token
	}
	fp = open('tokens.pkl', 'wb')
	pickle.dump(tokens, fp)
	fp.close()