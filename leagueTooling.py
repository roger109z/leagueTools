import requests
import socket
import time
import os
import queue

#so we don't have to see those pesky warnings telling me that localhost has no ssl certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
##########################################################################################

class leagueAPI:
    endpoints = {
        "auth": "/riotclient/auth-token",
        "runes": "/lol-perks/v1/pages",
        "acceptQueue": "/lol-matchmaking/v1/ready-check/accept",
        "rejectQueue": "/lol-matchmaking/v1/ready-check/decline",
        "echo": "/lol-game-session/v1/echo",
        "session": "/lol-gameflow/v1/session",
        "gameflowPhase": "/lol-gameflow/v1/gameflow-phase",
        "currentPage": "/lol-perks/v1/currentpage"
        
    }


    """
    Game Phases:
        Menu -> sitting in the main menu with no current lobby
        Lobby -> sitting in a lobby
        Matchmaking -> searching for a game
        ReadyCheck -> waiting for all players to accept the game
        ChampSelect -> selecting/banning champs
        InProgress -> Game running
        WaitingForStats -> between game closing and team honoring
        PreEndOfGame -> team honoring
        EndOfGame -> where you can see all the game stats

    """

    def __init__(self, dir="C:\\Riot Games\\League of Legends\\Logs\\LeagueClient Logs", url=None):
        
        if not url:
            self.url = self.getURL(dir)
        print("url is: " + self.url)

        self.firstRun = 0

        if self.isRunning():
            self.authToken = self.getAuthToken()

            self.gamestate = self.getGamestate()
        else:
            self.gamestate = ""

    def isRunning(self):
        out = True
        try:
            (requests.get(self.url + self.endpoints['echo'], verify=False))
        except requests.exceptions.ConnectionError:
            out = False
        return out
            

    def mainLoop(self, UIQueue, clientQueue, updateSpeed=50):
        delay = 60/updateSpeed
        lastGamestate = self.gamestate
        UIQueue.put(["state", lastGamestate])
        while self.isRunning():
            curState = self.getGamestate()
            if lastGamestate != curState:
                UIQueue.put(["state", curState])
                self.gamestate = curState
                print(lastGamestate + " -> " + curState)
                lastGamestate = curState

            time.sleep(delay)
        
        print("Game Closed")


    def setRunePage(self, page):
        if self.getCurrentRunepage()['isEditable']:
            print(requests.delete(self.url + self.endpoints["runes"] + "/" + str(self.getCurrentRunepage()['id']), verify=False).text)
            print(requests.post(self.url+self.endpoints["runes"], json=page, verify = False).text)

    def getGamestate(self):
        resp = requests.get(self.url + self.endpoints['session'], verify=False).json()

        if not "phase" in resp:
            return "Menu"
        else:
            return resp["phase"]
        

    def getURL(self, dir):
        files = os.listdir(dir)
        url = "https://riot:"
        for file in reversed(files):
            if file.endswith("LeagueClientUx.log"):
                with open(os.path.join(dir, file), "r") as f:
                    contents = f.read()
                    url += contents.split("https://riot:")[1].split('/')[0]
                    return url
        
    def getRunepageInfo(self):
        tmpPages = requests.get(self.url+self.endpoints["runes"], verify=False).json()
        outPages = []
        for page in tmpPages:
            if page["isEditable"]:
                outPages.append(page)
        return outPages
        
    def getCurrentRunepage(self):
        pages = self.getRunepageInfo()
        for page in pages:
            if page["current"]:
                return page

    def getAuthToken(self):
        return requests.get(self.url+self.endpoints["auth"], verify=False).text

    def acceptQueue(self):
        if self.gamestate == "ReadyCheck":
            print("accepting queue")
            return requests.post(self.url + self.endpoints["acceptQueue"], verify=False)

    def rejectQueue(self):
        if self.gamestate == "ReadyCheck":
            print("rejecting queue")
            return requests.post(self.url + self.endpoints["rejectQueue"], verify=False)

