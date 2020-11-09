import requests
import socket
import os
import keyboard

#so we don't have to see those pesky warnings telling me that localhost has no ssl certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

####changeable constants####

riotDirectory = "C:\\Riot Games\\League of Legends\\Logs\\LeagueClient Logs"

#################

endpoints = {
    "auth": "/riotclient/auth-token",
    "runes": "/lol-perks/v1/pages"
}

def getURL(dir):
    files = os.listdir(dir)
    url = "https://riot:"
    for file in reversed(files):
        if file.endswith("LeagueClientUx.log"):
            with open(os.path.join(dir, file), "r") as f:
                contents = f.read()
                url += contents.split("https://riot:")[1].split('/')[0]
                return url
    
def getAuthToken(url):
    return requests.get(url+endpoints["auth"], verify=False).text

url = getURL(riotDirectory)

print("url is: " + url)

#print(getAuthToken(url))

def acceptQueue():
    print("acceptQueue")

def waitForKeys():
    while True:
        try:
            if keyboard.is_pressed('space'):
                acceptQueue()
                
            elif keyboard.is_pressed('q'):
                break
        except:
            break

waitForKeys()

#

#resp = requests.get(url+endpoints["runes"], verify=False)

#print(resp.json())