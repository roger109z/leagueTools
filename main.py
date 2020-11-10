import leagueTooling
import keyboard
import time

def waitForKeys():

    api = leagueTooling.leagueAPI()

    keyboard.add_hotkey('space', lambda: api.acceptQueue())
    keyboard.add_hotkey('backspace', lambda: api.rejectQueue())

    api.mainLoop()

waitForKeys()