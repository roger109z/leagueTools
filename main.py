import leagueTooling
import keyboard
import time
import tkinter as tk
import threading
import queue

def startLeagueLoop(UIQueue, clientQueue):
    api = leagueTooling.leagueAPI()

    keyboard.add_hotkey('space', lambda: api.acceptQueue())
    keyboard.add_hotkey('backspace', lambda: api.rejectQueue())

    api.mainLoop(UIQueue, clientQueue)

def checkAlive(thread, win, updateSpeed):
    if thread.is_alive():
        win.after(updateSpeed, checkAlive, thread, win, updateSpeed)
    else:
        win.quit()

def updateInfo():
    try:
        event = UIQueue.get(block=False)
        if event[0] == "state": 
            bar["text"] = event[1]
        win.after(updateSpeed, updateInfo)
    except:
        win.after(updateSpeed, updateInfo)
    


win = tk.Tk()

UIQueue = queue.Queue()
clientQueue = queue.Queue()

clientLoop = threading.Thread(target=startLeagueLoop, args=(UIQueue, clientQueue))
clientLoop.daemon = True
clientLoop.start()

bar = tk.Label(win, text="Menu", bd=1, relief=tk.FLAT, anchor=tk.W)
bar['background'] = "#212121"
bar['fg'] = "cyan"
bar.pack(side=tk.BOTTOM, fill=tk.X)

updateSpeed = 1000
win.after(updateSpeed, updateInfo)
win.after(updateSpeed, checkAlive, clientLoop, win, updateSpeed)
win.title("League Tooling")
win.resizable(False, False)
win.geometry("900x700")
win['background'] = "#212121"
win.mainloop()
