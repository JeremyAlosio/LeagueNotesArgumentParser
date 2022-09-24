from ast import arg
from collections import deque
import os, time
import PySimpleGUI as sg                       
import tkinter as tk  
import threading
import winsound
import pyperclip


########################################################################################
###########################   Global Values Functionality  #############################
########################################################################################

nf = "C:\Riot Games\League of Legends\MyNotes.txt" #Set Notes File Location
switch = True
root = tk.Tk()
currentTime = 0
spellCooldownList = []
saveToClipboard = False
allThreads = []

########################################################################################
##############################   Resuable Functionality  ###############################
########################################################################################

def secondsToMinSeconds(time):
    minutes = int(time / 60)
    seconds = time - (minutes * 60)
    
    formattedTime = str(minutes) + ":" + str(seconds)
    
    return formattedTime


def timeStringToSeconds(timeString):
    if "," in timeString:
        timeArray = timeString.split(",")
        minutes = int(timeArray[0])
        seconds = int(timeArray[1])
        return (minutes * 60) + seconds
    else:
        return int(timeString)

    


########################################################################################
##############################   Alarm Functionality  ##################################
########################################################################################


def playAlarmSound():
    frequency = 500  # Set Frequency To 2500 Hertz
    duration = 500  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)

def alarmArg(codeArray):
    print("Alarm Arg Detected")
    
    try:
        alarmTimeOffset = int(codeArray[1])
    except:
        print("No Time Argument Set: Defaulting to 25 seconds.")
        alarmTimeOffset = 25

    def run():
        global currentTime
        
        try:
            goaltime = currentTime + alarmTimeOffset
            
            while (switch == True):
                time.sleep(1)
                if goaltime <= currentTime:
                    playAlarmSound()
                    break
                
                if switch == False:
                    break
        except:
            print("Game Timers not Set, Alarm Not Set")


    thread = threading.Thread(target=run)
    thread.start()
    
    global allThreads
    allThreads.append(thread)
                       

########################################################################################
###########################   Game Timer Functionality  ################################
########################################################################################



def gameTimerTracker(offset):
    def run():
        global currentTime
        currentTime = 0 + offset
        while (switch == True):
            time.sleep(1)
            currentTime += 1
            if switch == False:
                currentTime = 0
                break

    thread = threading.Thread(target=run)
    thread.start()
    
    global allThreads
    allThreads.append(thread)

def gameTimerArg(codeArray):
    print("Game Time Arg Detected")
    match len(codeArray):
        case 1:
            gameTimerTracker(0)
        case 2:
            gameTimerTracker(int(codeArray[1]))
            


########################################################################################
#######################   Spell Cooldown Tracker Functionality  ########################
########################################################################################

class SpellType:
    def __init__(self, name, cooldown):
        self.name = name
        self.cooldown = cooldown

class Spell:
    def __init__(self, spell, owner, gameTimeExperation):
        self.spell = spell
        self.owner = owner
        self.gameTimeExperation = gameTimeExperation
        
    def __str__(self) -> str:
        if self.owner != "":
            return self.owner.title() + " " + self.spell.name + ": " + secondsToMinSeconds(self.gameTimeExperation)
        else:
            return self.spell.name + ": " + secondsToMinSeconds(self.gameTimeExperation)

########### Spell Definitions ##########    

Flash = SpellType("Flash", 300)
Heal = SpellType("Heal", 240)
Ghost = SpellType("Ghost", 210)
Teleport = SpellType("Teleport", 360)
Cleanse = SpellType("Cleanse", 210)
Exhaust = SpellType("Exhaust", 210)
Barrier = SpellType("Barrier", 180)
Ignite = SpellType("Ignite", 180)

########################################    
  
def addSpellToCooldownList(spell):
    global spellCooldownList
    spellCooldownList.append(spell)
    
    
def keepClipboardUpToDate():
    global spellCooldownList
    
    formattedSpells = ""
    
    for spell in spellCooldownList:
        if spell.gameTimeExperation < currentTime:
            spellCooldownList.remove(spell)
        else:
            formattedSpells += str(spell) + " | "
    
    formattedSpells = formattedSpells[:-3]
    
    if saveToClipboard:
        pyperclip.copy(formattedSpells)
    

def parseSpellArgs(argSet, Spell):
    global currentTime
    
    try:
        argument = argSet[0]
        match argument:
            case "o" | "owner":
                Spell.owner = argSet[1]                   
            case "f" | "offset":
                Spell.gameTimeExperation = int(argSet[1]) + currentTime + Spell.spell.cooldown
            case "t" | "time":
                Spell.gameTimeExperation = timeStringToSeconds(argSet[1]) + currentTime + Spell.spell.cooldown

    except Exception as e: 
        print(e)
        return

def spellCooldownArg(codeArray):
    print("Spell Arg Detected")
    
    global currentTime
    
    spellDetected = False
    ownerDetected = False
    offsetDetected = False
    orginalTimeUsedDetected = False
    
    
    spellArgString = codeArray[1].lower()   
    currentSpellType = None
    
    match spellArgString: 
        case "f" | "fl" | "flash":
            currentSpellType = Flash
        case "h" | "hl" | "heal":
            currentSpellType = Heal
        case "g" | "gh" | "ghost":
            currentSpellType = Ghost
        case "t" | "tp" | "teleport":
            currentSpellType = Teleport
        case "c" | "cl" | "cleanse":
            currentSpellType = Cleanse
        case "e" | "ex" | "exhaust":
            currentSpellType = Exhaust
        case "b" | "br" | "barrier":
            currentSpellType = Barrier
        case "i" | "ig" | "ignite":
            currentSpellType = Ignite
    
    
    currentSpell = Spell(currentSpellType, "", currentTime + currentSpellType.cooldown)
    
    #ArgSet 1    
    try: 
        argSet = [codeArray[2], codeArray[3]]
        parseSpellArgs(argSet, currentSpell)
        
        try: 
            argSet = [codeArray[4], codeArray[5]]
            parseSpellArgs(argSet, currentSpell)
        except:
            pass
            
    except:
        print("No further Args found keeping current time as used time")
    
    print(currentSpell)
    addSpellToCooldownList(currentSpell)


    
########################################################################################
###############################   MyNotes.txt Parser  ##################################
########################################################################################

def tail(filename):
    with open(filename) as f:
        return deque(f, 1) 



def parseCode(code):
    codeArray = code.split()
    arg = codeArray[0].lower()
    match arg:
        case "gt":
            gameTimerArg(codeArray)
        case "a":
            alarmArg(codeArray)
        case "s":
            spellCooldownArg(codeArray)
        




########################################################################################
################################  Main  Loop ###########################################
########################################################################################
def pole():
    def run():
        moddate = os.stat(nf)[8]
        while (switch == True):
            newModdate = os.stat(nf)[8]
            keepClipboardUpToDate()
            if(moddate < newModdate):    
                try:
                    lastLine = tail(nf)[-1]
                    parseCode(lastLine)
                except Exception as e: 
                    print(e)
                moddate = newModdate
            time.sleep(1)
            if switch == False:
                break

    thread = threading.Thread(target=run)
    thread.start()
    
    global allThreads
    allThreads.append(thread)



########################################################################################
#############################  GUI Functionality  Loop #################################
########################################################################################

def switchon():  
    global switch
    global saveToClipboard
    switch = True
    saveToClipboard = True
    print('switch on')
    pole()  
      
def switchoff():  
    print('switch off')
    global switch
    switch = False    

def clipboardOn():  
    global saveToClipboard
    saveToClipboard = True
    print('clipboard on')

def clipboardOff():  
    print('clipboard off')
    global saveToClipboard
    saveToClipboard = False   

def kill():  
    global allThreads
    global switch
    switch = False 
    for thread in allThreads:
        thread.join()
        
    root.destroy()  
      
onbutton = tk.Button(root, text = "Pole ON", command = switchon)  
onbutton.pack()  
offbutton =  tk.Button(root, text = "Pole OFF", command = switchoff)  
offbutton.pack()  
clipboardOnbutton = tk.Button(root, text = "Clipboard Overwrite ON", command = clipboardOn)  
clipboardOnbutton.pack()  
clipboardoffbutton =  tk.Button(root, text = "Clipboard Overwrite OFF", command = clipboardOff)  
clipboardoffbutton.pack()  
killbutton = tk.Button(root, text = "EXIT", command = kill)  
killbutton.pack()  
      
root.mainloop()


