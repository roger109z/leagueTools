import leagueTooling
import keyboard

def waitForKeys():
    api = leagueTooling.leagueAPI()
    while True:
        try:
            if keyboard.is_pressed('space'):
                print(api.acceptQueue())
                
            elif keyboard.is_pressed('q'):
                break
        except:
            break

waitForKeys()