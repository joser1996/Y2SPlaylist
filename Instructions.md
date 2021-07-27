# Instructions
*Create a virtual environment if you want*
*Currently have to run shell.py from within shell/ otherwise .env isn't loaded properly.  
Make sure absolute paths are bing used and define them in .env file.*

```python
	python -m venv /path/to/new/virtual/environment
```
## Install Required dependencies from *requirements.txt*
```python
	python -m pip install -r requirements.txt
```

## Create .env file and Define following variables
* **GOOGLE_API_KEY**
* **YOUTUBE_CHANNEL_ID**
* **ROOT_FOLDER_PATH**
* **CLASS_FOLDER_PATH**
* **SPOTIFY_URI**
* **SPOTIFY_SECRET**
* **SPOTIFY_CLIENT**
* **DB_PASSWORD**


## Google Stuff  
Google account is necessary to use YouTube Data API.  
Go to developers.google.com and create a new project.  
First to get the

### GOOGLE_API_KEY
Go to Googles developer console [here](https://console.cloud.google.com/home/dashboard) and 
create a new project. Enable the **YouTube Data API** for the project you just created.
Create credentials for this project and get the API Key and store in .env file.
Go [here](https://developers.google.com/youtube/v3/getting-started) for more help with getting
started with the YouTube API.

### YouTube Stuff
Go to YouTube using the same Google account and go to 
* Settings
* Advanced Settings and get **Channel ID**. Create a channel if you don't have one.
Store this in **YOUTUBE_CHANNEL_ID** in .env  

## Folder Paths
**ROOT_FOLDER_PATH** is the absolute path to the directory of the project itself.
**CLASS_FOLDER_PATH** is the absolute path to the Classes/ in the project directory.  

## Spotify Stuff
Must have Spotify Account as well go to https://developer.spotify.com/dashboard/ and get Client ID and Spotify Secret
* Create a new App
	* Give it a name and a descripiton
* Go to edit settings and create a redirect uri.
	* Use: **http://localhost:8888/callback**
	* Make sure to add and save
This is what the backend uses to handle response  

### SPOTIFY_URI
Store URI you just created here in .env file  

### CLIENT ID and Secret
Get these from the app you just created in the dashboard.
Store them in .env file  

### Get Spotify Tokens
We need to get a refresh token and access token in order to use the api and modify your data.  
backend/server.py helps us get these things 
Go into backend/ and run server.py
* Open browser and go to *http://localhost:8888/request-auth*
* You should be prompted to login to your spotify account and give the app permission and asked to agree.
* You shold see window telling you it's ok to close now
* tokens.pkl  and origins.pkl file should have been created in backend/ this contains binary data  
  that holds both the Access Token and the Refresh Token
* Copy into **shell/** directory as they use the tokens. (Will eventually move this into my SQL database instead. pkl file for now)
You can alsoe create a database/ and put all the pkl files there and anything that needs access to 
them can get them from them. Define absolute path to this database/

## MySQL
I'm using MySQL to store a local copy of tracks that have been pushed to spotify to avoid
having redundant inserts everytime I pull songs from YouTube. If you want to use MySql you have to 
download it and reconfigure DBClient.py to use the proper user and your **DB_PASSWORD** are 
whatever you created when you set up MySQL.

Or you can rewrite code to use .pkl files for everything.
V1.0 of the app did it this way.
### DB Password
Used to when creating connection to mysql database

