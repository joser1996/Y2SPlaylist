import os
import json
import requests
import urllib
import base64
import time
import sys
import pickle
import re
class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authEndpoint = 'https://accounts.spotify.com/authorize?'
        self.tokenEndpoint = 'https://accounts.spotify.com/api/token'
        self.uri = os.environ.get('SPOTIFY_URI')
        self.uris = []

    def requestAuthorizationURL(self):
        getVars = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.uri,
            'scope': 'playlist-read-private playlist-modify-private'
        }
        url = self.authEndpoint + urllib.parse.urlencode(getVars)
        print(url)

    def requestTokens(self):
        code = os.environ.get('SPOTIFY_AUTH')
        body = {
            'grant_type': 'authorization_code',
            'code': code ,
            'redirect_uri': self.uri
        }

        response = requests.post(
            url,
            auth=(self.client_id, self.client_secret),
            data=body,
        )
        print(response.json())

    #request new token and save time of origin
    def refreshToken(self):
        url = 'https://accounts.spotify.com/api/token'
        r_token = os.environ.get('SPOTIFY_RT')

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': r_token
        }
        header= {
            'Authorization': 'application/x-www-form-urlencoded'
        }
        res = requests.post(
            url,
            auth=(self.client_id, self.client_secret),
            data=payload,
            headers=header
        )
        res_data = res.json()
        new_t = res_data.get('access_token')
        current_time = round(time.time())
        obj_to_save = {
            "origin": current_time
        }
        #save the origin time as a pkl file
        pickle_out = open("origin_time.pkl", "wb")
        pickle.dump(obj_to_save, pickle_out)
        pickle_out.close()

        #save the new token
        token_obj = {
            "token": new_t
        }
        pkl_out = open("access_token.pkl", "wb")
        pickle.dump(token_obj, pkl_out)
        pkl_out.close()

    def getCurrentToken(self):
        fp = open("access_token.pkl", "rb")
        token = pickle.load(fp)
        fp.close()
        return token['token']


    def refreshAccessToken(self):
        pickle_in = open("origin_time.pkl", "rb")
        obj = pickle.load(pickle_in)

        origin_time = obj["origin"]
        current_time = round(time.time())
        delta_time = current_time - origin_time
        ONE_HOUR = 3600
        if (delta_time > ONE_HOUR or current_time < origin_time ):
            print("Refreshing TOKEN")
            self.refreshToken()
        else:
            print("Token is fresh.")

    # Method to insert a song or possiblly a list of songs
    #default to the test playlist
    def insertSongs(self, songs, id='5O7l46N1wPZuqHDjOygRuF'):
        endPoint = 'https://api.spotify.com/v1/playlists/' + id +'/tracks'
        a_token = self.getCurrentToken()
        ar = []
        for song in songs:
            try:
                uri = self.getTrackURI(song)
                ar.append(uri)
            except:
                print("Song: ", song, " NOT FOUND!")

        #print("URIS: ", ar)
        self.uris = ar
        if not ar:
            return

        body = {'uris': ar, 'position': 0}
        header = {
            'Authorization': 'Bearer {}'.format(a_token),
            'Content-Type': 'application/json'
        }
        res = requests.post(
            url=endPoint,
            json=body,
            headers=header
        )
        print("Insert Response: ", res.json())


    def getTrackURI(self, songName):
        #this is a GET request
        endPoint = 'https://api.spotify.com/v1/search?'
        header = {'Authorization': 'Bearer ' + self.getCurrentToken()}
        q = self.makeQuery(songName)
        print("Q: ", q)
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


    def getPlaylists(self):
        url = 'https://api.spotify.com/v1/me/playlists'
        #load in the current access token
        pickle_in = open("access_token.pkl", "rb")
        token_obj = pickle.load(pickle_in)
        a_token = token_obj['token']
        pickle_in.close()
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + a_token
        }
        response = requests.get(
            url=url,
            headers=header
        )
        res_json = response.json()
        pls = {}
        try:
            for item in res_json["items"]:
                id = item['id']
                name = item['name']
                pls[id] = name
        except:
            print("updateMyPlaylists Failed")
            print(res_json)
        pickle_out = open("playlists.pkl", "wb")
        pickle.dump(pls, pickle_out)
        pickle_out.close()

    def printPlaylists(self):
        pickle_in = open("playlists.pkl", "rb")
        dict = pickle.load(pickle_in)
        for id in dict:
            print(dict[id])
        pickle_in.close()
# TODO:  Look at response or figure out which songs were successfully inserted
 