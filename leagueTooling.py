import requests
import socket
import os


#so we don't have to see those pesky warnings telling me that localhost has no ssl certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
##########################################################################################

class leagueAPI:
    endpoints = {
        "auth": "/riotclient/auth-token",
        "runes": "/lol-perks/v1/pages",
        "acceptQueue": "/lol-matchmaking/v1/ready-check/decline"
    }


    def __init__(self, dir=None, url=None):
        if not url:
            if not dir:
                dir = "C:\\Riot Games\\League of Legends\\Logs\\LeagueClient Logs"
            self.url = self.getURL(dir)
        print("url is: " + self.url)

        self.authToken = self.getAuthToken()

    def getURL(self, dir):
        files = os.listdir(dir)
        url = "https://riot:"
        for file in reversed(files):
            if file.endswith("LeagueClientUx.log"):
                with open(os.path.join(dir, file), "r") as f:
                    contents = f.read()
                    url += contents.split("https://riot:")[1].split('/')[0]
                    return url
        
    def getAuthToken(self):
        return requests.get(self.url+self.endpoints["auth"], verify=False).text

    def acceptQueue(self):
        return requests.post(self.url + self.endpoints["acceptQueue"], verify=False)

