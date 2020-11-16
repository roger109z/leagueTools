import leagueTooling
import keyboard
import time
import tkinter as tk
from tkinter import ttk
import threading
import queue
import os
import json

def startLeagueLoop(UIQueue, clientQueue):
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
    
def getRunes():
    return api.getCurrentRunepage()

def getSavedRunes():
    try:
        if os.path.exists("runes.json"):
            with open("runes.json", "r") as runes:
                return json.loads(runes.read())
        else:
            return {}
    except:
        return {}

def savePages(runes):
    with open("runes.json", "w") as runes_file:
        runes_file.write(json.dumps(runes))

def addPage():
    runes = getSavedRunes()
    pageToSave = getRunes()
    print("saving: " + pageToSave['name'])
    runes[pageToSave['name']] = pageToSave
    savePages(runes)

def loadPage(var):
    pages = getSavedRunes()
    name = var.get()
    if name in pages:
        print("Loading: " + name)
        api.setRunePage(pages[name])


def updateRuneSelection(selectionMenu, var):
    runes = getSavedRunes()
    selectionMenu['menu'].delete(0, "end")
    for key in runes:
        selectionMenu['menu'].add_command(label=str(key), command=lambda name=key: runepageSelected.set(str(name)))


    fkey = "\t\t\t"
    for key in runes:
        fkey = key
        break
    var.set(fkey)

def addAndUpdateRunes(selectionMenu, var):
    addPage()
    updateRuneSelection(selectionMenu, var)

api = leagueTooling.leagueAPI()

win = tk.Tk()
win.tk.call('lappend','auto_path','themes')
win.tk.call('package','require','awdark')

style = ttk.Style()
style.theme_use('awdark')

mainframe = ttk.Frame(win)
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
win.columnconfigure(0, weight=1)
win.rowconfigure(0, weight=1)

nbook = ttk.Notebook(mainframe)
nbook.grid()

UIQueue = queue.Queue()
clientQueue = queue.Queue()

clientLoop = threading.Thread(target=startLeagueLoop, args=(UIQueue, clientQueue))
clientLoop.daemon = True
clientLoop.start()

###RUNES###
runeframe = ttk.Frame(nbook)
nbook.add(runeframe, text="Runes",sticky='nsew')

runepages = []
for key in getSavedRunes():
    runepages.append(key)

runepageSelected = tk.StringVar()
selection = ttk.OptionMenu(runeframe, runepageSelected, "\t\t\t", *runepages)

selection.grid(column=0, row=2)

load = ttk.Button(runeframe, text="Load", command=lambda: loadPage(runepageSelected))
load.grid(column=1, row=2)

save = ttk.Button(runeframe, text="Save", command=lambda: addAndUpdateRunes(selection, runepageSelected))
save.grid(column=0, row=3)

###########

###GAMEINFO###

gameInfoFrame = ttk.Frame(nbook)
nbook.add(gameInfoFrame, text="Game", sticky='nsew')


##############

###BOTTOM BAR###
statusBar = ttk.Frame(win)
statusBar.grid(column=0, row=1, sticky=(tk.W, tk.E))

bar = ttk.Label(statusBar, text="Menu")
bar.grid(column=0, row=3, sticky=(tk.S))
################

updateSpeed = 1000
win.after(updateSpeed, updateInfo)
win.after(updateSpeed, checkAlive, clientLoop, win, updateSpeed)
win.title("League Tooling")
win.resizable(False, False)
win.geometry("900x700")
win.mainloop()
