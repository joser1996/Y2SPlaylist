import os
import json
import requests
import urllib
import base64
import time
import sys
import pickle
import re
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path("../.env"))
sys.path.append(os.environ.get('ROOT_FOLDER_PATH'))
from helpers import *

class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    """
    Method inserts songs in spotify playlist with id: id
    @songs: [string] -  an array of song titles
    @id: string - the playlist id to which songs will be added
    return: track_uris:[string] uris of songs that were added to spotify
    """
    def insertSongs(self, songs, id):
        endPoint = 'https://api.spotify.com/v1/playlists/' + id +'/tracks'
        tokens = pickle.load(open('tokens.pkl', 'rb'))
        a_token = self.getCurrentToken()
        track_uris = []
        ret = {}
        for song in songs:
            try:
                uri = self.getTrackURI(song)
                track_uris.append(uri)
                ret[uri] = song
            except:
                print("Song: ", song, " NOT FOUND!")
        if not track_uris:
            return None

        body = {'uris': track_uris, 'position': 0}
        header = {
            'Authorization': 'Bearer {}'.format(a_token),
            'Content-Type': 'application/json'
        }
        res = requests.post(
            url=endPoint,
            json=body,
            headers=header
        )

        return ret 

    #return: tokens:string
    def getCurrentToken(self):
        tokens = pickle.load(open('tokens.pkl', 'rb'))
        return tokens['access_token']

    def getTrackURI(self, songName):
        #this is a GET request
        endPoint = 'https://api.spotify.com/v1/search?'
        header = {'Authorization': 'Bearer ' + self.getCurrentToken()}
        q = self.makeQuery(songName)
        #print("Q: ", q)
        url = endPoint + q
        res = requests.get(url=url, headers=header)
        res_json = res.json()
        #print(json.dumps(res_json, indent=2))
        return res_json['tracks']['items'][0]['uri']

    def makeQuery(self, songName):
        #attempt to seperate into artist and song
        query = "q="
        #some pre processing remove (), anything after ft.
        splitString = songName.split("ft.")[0]
        if splitString:
            songName = splitString

        splitString = songName.split("(")[0]
        if splitString:
            songName = splitString

        splitString = songName.split("[")[0]
        if splitString:
            songName = splitString
        try:
            maxSplit = 1
            splittedString = songName.split('-', maxSplit)
            if splittedString[1][0] == ' ':
                splittedString[1] = splittedString[1][1:]

            artist = splittedString[0].replace(" ", "%20")
            trackName = splittedString[1].replace(" ", "%20")
            query = query + "artist:" + artist
            query = query + "track:" + trackName
            query = query + "&type=track&limit=1"
            return query
        except:
            trackname = songName.replace(" ", "%20")
            query = query + "track:" + trackName + "&type=track&limit=1"
            return query

    #return: ret:[(string, int)] returns all playlist names with their associated id
    def getPlaylists(self):
        url = 'https://api.spotify.com/v1/me/playlists'
        #load in the current access token
        access_token = self.getCurrentToken()
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }
        response = requests.get(
            url=url,
            headers=header
        )
        res_json = response.json()
        ret = []
        try:
            for item in res_json["items"]:
                plId = item['id']
                name = item['name']
                ret.append((name, plId))
        except:
            print("getPlaylists Failed")
            print(res_json)

        return ret

    def createPlaylist(self, name = None, desc = "N/A"):
        if not name:
            msg = "Must provide playlist Name"
            response = {"status": False, "Message": msg}
            return response
        if not tokenIsFresh():
            refreshAccessToken()
        user_id = self.getUserId()
        endPoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        access_token = self.getCurrentToken()
        header = {
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json"
        }
        body ={
            "name": name,
            "public": False,
            "description": desc
        }
        response = requests.post(
            url=endPoint,
            json=body,
            headers=header
        )
        print("Response: ", response)
        print()
        print("JSON", response.json())
        return {"status": True, "Message": "Done"}

    #This is the same as unfollowing a playlist
    def deletePlaylist(self, pl_id):
        endPoint = f"https://api.spotify.com/v1/playlists{pl_id}/followers"
        if not tokenIsFresh()
            refreshAccessToken()
        access_token = self.getCurrentToken()
        header = {
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json"
        }
        

    def getUserId(self):
        profile = self.getUserProfile()
        return profile["id"]

    def getUserProfile(self):
        endPoint = "https://api.spotify.com/v1/me"
        if not tokenIsFresh():
            refreshAccessToken()
        access_token = self.getCurrentToken()
        header = {
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json"
        }
        response = requests.get(
            url=endPoint,
            headers=header
        )
        userProfile = response.json()
        return userProfile
