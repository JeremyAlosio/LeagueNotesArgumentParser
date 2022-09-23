from collections import deque
import os, time
import PySimpleGUI as sg                       
import tkinter as tk  
import threading
import winsound

########################################################################################
###########################   Global Values Functionality  #############################
########################################################################################

nf = "C:\Riot Games\League of Legends\MyNotes.txt" #Set Notes File Location
switch = True
root = tk.Tk()
global currentTime


########################################################################################
##############################   Resuable Functionality  ###############################
########################################################################################

def currentTimeToMinSeconds():
    global currentTime
    minutes = currentTime / 60
    seconds = currentTime - (minutes * 60)
    
    formattedTime = minutes + ":" + seconds
    
    return formattedTime


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
            print(currentTime)
            if switch == False:
                currentTime = 0
                break

    thread = threading.Thread(target=run)
    thread.start()

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

class Spell:
    def __init__(self, name, cooldown):
        self.name = name
        self.cooldown = cooldown

class SpellAndOwner:
    def __init__(self, spell, owner):
        self.spell = spell
        self.owner = owner
    
Flash = Spell("Flash", 600)

def spellCooldownArg(codeArray):
    print("Spell Arg Detected")
    
    
    
    
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
            spellCooldownArg()
        




########################################################################################
################################  Main  Loop ###########################################
########################################################################################
def pole():
    def run():
        moddate = os.stat(nf)[8]
        while (switch == True):
            newModdate = os.stat(nf)[8]
            if(moddate < newModdate):    
                lastLine = tail(nf)[-1]
                parseCode(lastLine)
                moddate = newModdate
            time.sleep(0.5)
            if switch == False:
                break

    thread = threading.Thread(target=run)
    thread.start()



########################################################################################
#############################  GUI Functionality  Loop #################################
########################################################################################

def switchon():  
    global switch
    switch = True
    print('switch on')
    pole()  
      
def switchoff():  
    print('switch off')
    global switch
    switch = False    
      
def kill():  
    root.destroy()  
      
onbutton = tk.Button(root, text = "Pole ON", command = switchon)  
onbutton.pack()  
offbutton =  tk.Button(root, text = "Pole OFF", command = switchoff)  
offbutton.pack()  
killbutton = tk.Button(root, text = "EXIT", command = kill)  
killbutton.pack()  
      
root.mainloop()


