# League Notes Argument Parser

A simple program designed to enhance the functionality of the MyNotes.txt file found in League of Legends (accessed in game through the commands /n or /notes).

There are 3 Main Functionalities:

Game Timer: Keeps track of in game time
      Command: "gt" | "g" | "t" | "time" | "gametime"
      
          Argument: none
                Description: By adding no arguments the user simply starts the timer. It will increment by 1 every second after it has been started
          Argument: (Integer)
                Description: By adding an Integer the offset of the timer will begin from the inputed Integer

Alarm: Sets an Alarm that will go off after X time
      Command: "a" | "alarm"
      
          Argument: none
                Description: By adding no arguments the user will set a timer for 25 seconds in the future
          Argument: (Integer)
                Description: By adding only an Integer the offset of the alarm will go of X seconds in the future
          Argument: "t" | "time" + TIMEFORMAT*
                Description: By adding the Argument followed by an Integer the timer will go off at X seconds in game time

Spell Tracker: Tracks when defined Spells will be up based on user input
      Command: "s" | "spell"
      
          Argument: SPELLINPUT*
                Description: By adding a SPELLINPUT* only the timer will add that time to a timer and will copy the spell and time to the clipboard. The spell will be removed when the in game time for the spell to be up has passed.
          Argument: SPELLINPUT* + "o" | "owner" + (String)
                Description: When you add an Owner to the Spell it will label the spell as that person's spell and will display alongside the Spell timer
          Argument: SPELLINPUT* + "t" | "time" + (Integer)
                Description: Adding the time argument will add an offset to the current game time and start the spell timer from there

        





SPELLINPUT:
    Flash: "f" | "fl" | "flash"
    Heal: "h" | "hl" | "heal"
    Ghost: "g" | "gh" | "ghost"
    Teleport: "t" | "tp" | "teleport"
    Cleanse: "c" | "cl" | "cleanse"
    Exhaust: "e" | "ex" | "exhaust"
    Barrier: "b" | "br" | "barrier"
    Ignite: "i" | "ig" | "ignite"

  
TIMEFORMAT:
    Description: Custom time format is used in this app for speed
    Options: X,Y
    Options: X.Y - Unimplemented
    Options: X:Y - Unimplemented
    Options: X;Y - Unimplemented
