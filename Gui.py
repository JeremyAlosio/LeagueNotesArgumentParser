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
##############################   Alarm Functionality  ##################################
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
###########################   Game Timer Functionality  ################################
########################################################################################

def playAlarmSound():
    frequency = 500  # Set Frequency To 2500 Hertz
    duration = 500  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)

def alarmArg(codeArray):
    alarmTimeOffset = int(codeArray[1])
    def run():
        global currentTime
        goaltime = currentTime + alarmTimeOffset
        while (switch == True):
            time.sleep(1)
            if goaltime <= currentTime:
                playAlarmSound()
            
            if switch == False:
                currentTime = 0
                break

    thread = threading.Thread(target=run)
    thread.start()


########################################################################################
#######################   Spell Cooldown Tracker Functionality  ########################
########################################################################################
  
def SpellCooldownArg():
    print("Spell Arg Detected")
    
    
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
            print("Alarm Arg Detected")
            alarmArg(codeArray)

        case "s":
            print("Spell Arg Detected")
        




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


