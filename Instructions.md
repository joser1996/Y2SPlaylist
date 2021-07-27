# Instructions
*Create a virtual environment if you want using*
*Currently have to run shell.py from within shell/ otherwise .env isn't loaded properly. Fix by using absolute path.*

```python
	python -m venv /path/to/new/virtual/environment
```
## Install Required dependencies from *requirements.txt*
```python
	python -m pip install -r requirements.txt
```

## Create .env file and Define following variables
Variables used is .env file  


## Google Stuff  
Google account is necessary to use YouTube Data API.
* Go to developers.google.com and create a new project.



## GOOGLE_API_KEY
Helpful article https://developers.google.com/youtube/v3/getting-started towards getting
In newly created app create credentials, public only for now, and get the api key
For now you have to go to your youtube account associated with same google email used to create
your API key. Go to
* Settings
* Advanced Settings and get **Channel ID**. Create a channel if you don't have one.
store in **YOUTUBE_CHANNEL_ID** in .env  

## Spotify Stuff
Must have Spotify Account as well go to https://developer.spotify.com/dashboard/ and get Client ID and Spotify Secret
* Create a new App
	* Give it a name and a descripiton
* Go to edit settings and create a redirect uri.
	* Use: **http://localhost:8888/callback**
	* Make sure to add and save
This is what the backend uses to handle response
## SPOTIFY_URI
Store URI you just created here in .env file
## CLIENT ID and Secret
Get these from the app you just created in the dashboard
Store them in
## SPOTIFY_CLIENT_ID and SPOTIFY_SECRET respectivly
### Get Spotify Tokens
We need to get a refresh token and access token in order to use the api and modify your data. backend/server.py helps us get these things 
Go into backend/ and run server.py
* Open browser and go to *http://localhost:8888/request-auth*
* You should be prompted to login to your spotify account and give the app permission and asked to agree.
* You shold see window telling you it's ok to close now
* tokens.pkl file should have been created in backend/ this contains binary data that holds both the Access Token and the Refresh Token
* Copy into **shell/** directory as they use the tokens. (Will eventually move this into my SQL database instead. pkl file for now)
You can create a database/ and put all the pkl files there when they are needed. Use absolute path to this directory
** Where do the pkl files go **

## DB Password
Used to when creating connection to mysql database


TOKENS_URI
SPOTIFY_AUTH
SPOTIFY_RT
ROOT_FOLDER_PATH
CLASS_FOLDER_PATH