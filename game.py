# Author: Jovan Petreski
# Date finished: 12/12/2019
# Product type: Tkinter game
# A short description of the game: you are playing as a shark
# in a very polluted ocean (with lots of cans and plastic bags)
# Your task is to survive as long as possible (that is without
# eating any of the unwanted objects) and possibli eat as many
# fish as possible (so that your score increases). At the
# beginning, you are displayed 4 menus: start new game, load
# last saved game, leaderboard and quit. You can also save your
# current game but be aware that this deletes the previous saved
# game. If you are in the top 5 players, your name will be
# displayed in the leaderboard. There are 3 cheat codes: nodeath
# (you can lose the game), double (the score for each fish eaten
# is now twice than normally) and noobject (only fish will be
# created for you and the ocean suddenly becomes very clear :).
# You can pause and unpause the game only when in gameplay mode and
# you have a boss key at your disposal all the time.

from tkinter import *
from random import randint
import sys
import os
import time

# Score and level: displayed on canvas
score = 0
level = 1
scoreText = None
levelText = None

userNameText = None
GameOver = None
Counting = None
pauseTxt = None

# Rectangles representing the menus used
# in the game
startMenu = None
leaderboardMenu = None
loadMenu = None
quitMenu = None

# Menus that appear after a game or during pause
againMenu = None
mainMenu = None
saveMenu = None

# A text box
enterUsername = None

# The text inside the menus
startText = None
loadText = None
leaderboardText = None
quitText = None

# Text inside other menus (pause and game over page)
againText = None
mainText = None
saveText = None

# Booleans used to determine when to display
# certain objects
gameOver = False
canStart = False
countOn = False
gameOn = False
menusOn = True
loadedGame = False
pause = False
canGo = False
bossOn = False

# Used to activate the cheats
noDeath = False
doubleScore = False
noObstacles = False

mainObject = None   # The shark
screenshot = None   # Image used to display when pressed boss key

# The max possibility each of the object can be created.
# Modified as the user progresses.
canMaxChance = 120
fishMaxChance = 125
bagMaxChance = 130
nextLevel = 100  # Used to update level

# Lists containing all the moving objects on canvas
cans = list()
allFish = list()
bags = list()
bubbles = list()

# =================== Binding functions =========================


def leftKey(event):     # Move leftwards
    global pause
    if (gameOn and not gameOver and not ldrbOn and not menusOn):
        curr_pos = canvas.coords(mainObject)[0]
        if (curr_pos - 10 >= 0 and not pause and canGo and not gameOver):
            canvas.move(mainObject, -10, 0)
    return


def rightKey(event):    # Move rightwards
    global pause
    if (gameOn and not gameOver and not ldrbOn and not menusOn):
        curr_pos = canvas.coords(mainObject)[0]
        if (curr_pos + 210 <= sWidth and not pause and canGo and not gameOver):
            canvas.move(mainObject, 10, 0)
    return


def upKey(event):       # Move upwards
    global pause
    if (gameOn and not gameOver and not ldrbOn and not menusOn):
        curr_pos = canvas.coords(mainObject)[1]
        if (curr_pos - 100 >= 0 and not pause and canGo and not gameOver):
            canvas.move(mainObject, 0, -10)
    return


def downKey(event):     # Move downwards
    global pause
    if (gameOn and not gameOver and not ldrbOn and not menusOn):
        curr_pos = canvas.coords(mainObject)[1]
        if (curr_pos+300 <= sHeight and not pause and canGo and not gameOver):
            canvas.move(mainObject, 0, 10)
    return


def cheatKey(event):    # No death
    global noDeath

    # The same code is used to activate and deactivate the cheat
    if (not noDeath):
        noDeath = True
    else:
        noDeath = False
    return


def cheatKey2(event):   # Double score
    global doubleScore

    # Same code to deactivate the cheat
    if (not doubleScore):
        doubleScore = True
    else:
        doubleScore = False


def cheatKey3(event):   # Only fish will be created
    global noObstacles

    # Same code to deactivate
    if (not noObstacles):
        noObstacles = True
    else:
        noObstacles = False


def exitKey(event):     # In case quit is pressed
    window.quit()


def pauseKey(event):    # Escape button is pressed
    global pause
    global gameOver
    global pauseTxt
    global countOn
    global saveText
    global mainText
    global saveMenu
    global mainMenu

    if (not gameOver and not countOn and not ldrbOn and not menusOn):
        if (pause):     # Deactivate pause
            canvas.delete(pauseTxt)
            canvas.delete(saveText)
            canvas.delete(mainText)
            canvas.delete(saveMenu)
            canvas.delete(mainMenu)
            canvas.pack()

            countOn = True
            window.after(50, countdown, 3)
            pause = False
            window.after(4000, createMove)
        else:   # Activate Pause
            pause = True    # Display pause text
            pauseTxt = canvas.create_text(sWidth/2, sHeight/2,
                                          fill="white", font="Times 60 bold",
                                          text="Paused")

            save_x1 = (sWidth / 3) - 150
            save_y1 = 2*(sHeight / 3) - 30
            save_x2 = save_x1 + 300
            save_y2 = save_y1 + 60

            # Display save menu
            saveMenu = canvas.create_rectangle(save_x1, save_y1,
                                               save_x2, save_y2,
                                               fill="steel blue",
                                               outline="white")
            saveText = canvas.create_text((save_x1 + save_x2)/2,
                                          (save_y1 + save_y2)/2,
                                          fill="white",
                                          font="Times 20 bold",
                                          text="Save Game")

            main_x1 = 2*(sWidth/3) - 150
            main_y1 = 2*(sHeight / 3) - 30
            main_x2 = main_x1 + 300
            main_y2 = main_y1 + 60

            # Display back to main menu
            mainMenu = canvas.create_rectangle(main_x1, main_y1,
                                               main_x2, main_y2,
                                               fill="steel blue",
                                               outline="white")
            mainText = canvas.create_text((main_x1 + main_x2)/2,
                                          (main_y1 + main_y2)/2,
                                          fill="white",
                                          font="Times 20 bold",
                                          text="Return to home page")
            canvas.pack()
            return


def bossKey(event):     # Enter (Return) is used as a boss key
    global pause
    global gameOver
    global pauseTxt
    global gameOn
    global menusOn
    global countOn
    global Counting
    global ldrbOn
    global bossOn
    global screenshot

    # When boss key is pressed, activate the pause
    if (not gameOver and not pause and not menusOn and not ldrbOn):
        pause = True
        countOn = False
        canvas.delete(Counting)
        pauseTxt = canvas.create_text(sWidth/2, sHeight/2,
                                      fill="white",
                                      font="Times 60 bold",
                                      text="Paused")
    if (bossOn):
        bossOn = False
        canvas.delete(screenshot)
        canvas.pack()
    else:
        bossOn = True
        screenshot = canvas.create_image(0, sHeight, anchor=SW,
                                         image=screenshotImg)
        canvas.pack()


def clickEvent(event):  # Handling the clicking event (menu pages)
    global gameOn
    global gameOver
    global pause
    global level
    global canMaxChance
    global bagMaxChance
    global fishMaxChance
    global nextLevel
    global score
    global ldrbOn
    global menusOn
    global loadedGame

    # When to display main menu
    if (not gameOn and not ldrbOn and menusOn):
        x = event.x
        y = event.y

        # Get the coordinates of each menu
        start_x1 = sWidth / 2 - 300
        start_y1 = sHeight / 4 - 50
        start_x2 = start_x1 + 600
        start_y2 = start_y1 + 100

        load_x1 = start_x1
        load_y1 = start_y2 + 40
        load_x2 = start_x2
        load_y2 = load_y1 + 100

        ldr_x1 = start_x1
        ldr_y1 = load_y2 + 40
        ldr_x2 = start_x2
        ldr_y2 = ldr_y1 + 100

        quit_x1 = start_x1
        quit_y1 = ldr_y2 + 40
        quit_x2 = start_x2
        quit_y2 = quit_y1 + 100

        # In case start was pressed
        if (x >= start_x1 and x <= start_x2):
            if (y >= start_y1 and y <= start_y2):
                level = 1
                canMaxChance = 120
                bagMaxChance = 130
                fishMaxChance = 125
                nextLevel = 100
                score = 0
                menusOn = False
                gameOn = True
                ldrbOn = False
                loadedGame = False
                getUsername()

        # Quit was pressed
        if (x >= quit_x1 and x <= quit_x2):
            if (y >= quit_y1 and y <= quit_y2):
                quitGame()

        # Load game was pressed
        if (x >= load_x1 and x <= load_x2):
            if (y >= load_y1 and y <= load_y2):
                menusOn = False
                gameOn = True
                ldrbOn = False
                loadedGame = True
                loadGame()

        # Leaderboard was pressed
        if (x >= ldr_x1 and x <= ldr_x2):
            if (y >= ldr_y1 and y <= ldr_y2):
                ldrbOn = True
                menusOn = False
                leaderBoard()

    # Menus displayed after game over: play again and main menu
    if (gameOver and not ldrbOn and not gameOn and not menusOn):
        x = event.x
        y = event.y

        again_x1 = (sWidth / 3) - 150
        again_y1 = 2*(sHeight / 3) - 30
        again_x2 = again_x1 + 300
        again_y2 = again_y1 + 60

        main_x1 = 2*(sWidth/3) - 150
        main_y1 = 2*(sHeight / 3) - 30
        main_x2 = main_x1 + 300
        main_y2 = main_y1 + 60

        # Play again was pressed
        if (x >= again_x1 and x <= again_x2):
            if (y >= again_y1 and y <= again_y2):
                gameOn = True
                gameOver = False
                playAgain()

        # Back to homepage was selected
        if (x >= main_x1 and x <= main_x2):
            if (y >= main_y1 and y <= main_y2):
                canvas.delete("all")
                gameOn = False
                gameOver = False
                menusOn = True

                # Clear all the lists of objects
                cans.clear()
                allFish.clear()
                bags.clear()
                bubbles.clear()
                menuPage()

    # When pause is pressed
    if (pause and not ldrbOn):
        x = event.x
        y = event.y

        # Get coordinates
        save_x1 = (sWidth / 3) - 150
        save_y1 = 2*(sHeight / 3) - 30
        save_x2 = save_x1 + 300
        save_y2 = save_y1 + 60

        main_x1 = 2*(sWidth/3) - 150
        main_y1 = 2*(sHeight / 3) - 30
        main_x2 = main_x1 + 300
        main_y2 = main_y1 + 60

        # The user chose to save the current game
        if (x >= save_x1 and x <= save_x2):
            if (y >= save_y1 and y <= save_y2):
                saveGame()

        # The used opted to leave the game (main menu)
        if (x >= main_x1 and x <= main_x2):
            if (y >= main_y1 and y <= main_y2):
                canvas.delete("all")
                menusOn = True

                # Clear all the lists of objects
                cans.clear()
                allFish.clear()
                bags.clear()
                bubbles.clear()
                menuPage()
        return

    # A back button to the home page when leaderboard is on
    if (ldrbOn and not menusOn and not gameOn):
        x = event.x
        y = event.y

        back_x1 = 50
        back_y1 = 50
        back_x2 = back_x1 + 200
        back_y2 = back_y1 + 50

        if (x >= back_x1 and x <= back_x2):
            if (y >= back_y1 and y <= back_y2):
                canvas.delete("all")
                ldrbOn = False
                menuPage()


# ================== Helper functions ==========================


entry1 = None
button1 = None
username = None


def addUsername():  # A function that saves the entered username
    global entry1   # and starts the game
    global button1
    global username
    global enterUsername

    username = entry1.get()     # Get the username entered
    entry1.place_forget()
    button1.place_forget()
    canvas.delete(enterUsername)

    # We first have to bind all the keys again
    canvas.bind("<Left>", leftKey)
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.bind("<n><o><d><e><a><t><h>", cheatKey)
    canvas.bind("<Escape>", pauseKey)
    canvas.bind("<Return>", bossKey)
    canvas.bind("<d><o><u><b><l><e>", cheatKey2)
    canvas.bind("<n><o><o><b><j><e><c><t>", cheatKey3)
    canvas.bind("<Button-1>", clickEvent)
    canvas.focus_set()

    startPoint()    # Start the game
    return


def getUsername():  # A helper function to clear the canvas
    global entry1   # and create a text box for the username
    global button1
    global startMenu
    global loadMenu
    global leaderboardMenu
    global quitMenu
    global startText
    global loadText
    global leaderboardText
    global quitText
    global enterUsername

    # Clear the canvas of the menus
    canvas.delete(startText)
    canvas.delete(startMenu)
    canvas.delete(loadMenu)
    canvas.delete(loadText)
    canvas.delete(quitMenu)
    canvas.delete(quitText)
    canvas.delete(leaderboardMenu)
    canvas.delete(leaderboardText)

    # Unbind all the keys so they don't interfere when tying
    canvas.unbind("<Left>")
    canvas.unbind("<Right>")
    canvas.unbind("<Up>")
    canvas.unbind("<Down>")
    canvas.unbind("<n><o><d><e><a><t><h>")
    canvas.unbind("<Escape>")
    canvas.unbind("<Return>")
    canvas.unbind("<d><o><u><b><l><e>")
    canvas.unbind("<n><o><o><b><j><e><c><t>")
    canvas.unbind("<Button-1>")

    # Create the text box
    entry1 = Entry(canvas)
    entry1.place(x=sWidth/2, y=sHeight/2, anchor=CENTER)

    # When pressed the button, continue with the process
    button1 = Button(canvas, text="Submit", command=addUsername)
    button1.place(x=sWidth/2, y=sHeight/2 + 50, anchor=CENTER)
    enterUsername = canvas.create_text(sWidth/2, sHeight/3,
                                       fill="white",
                                       font="Times 30 bold",
                                       text="Enter username: ")
    return


def loadGame():     # Opens the file where the last saved game
    global level    # was stored and retrieves the data
    global canMaxChance
    global bagMaxChance
    global fishMaxChance
    global nextLevel
    global score
    global username

    # Open the file, read the data
    savedgame = open("savedgame.txt")
    prev_lvl = savedgame.readline()
    level = int(prev_lvl)
    prev_scr = savedgame.readline()
    score = int(prev_scr)
    prev_nxt = savedgame.readline()
    nextLevel = int(prev_nxt)
    prevCan = savedgame.readline()
    canMaxChance = int(prevCan)
    prev_fish = savedgame.readline()
    fishMaxChance = int(prev_fish)
    prev_bag = savedgame.readline()
    bagMaxChance = int(prev_bag)
    username = savedgame.readline()
    savedgame.close()   # Then close it
    startPoint()


# Globals used to create the leaderboard
top1_name = None
top2_name = None
top3_name = None
top4_name = None
top5_name = None
ldbrMenu = None
ldbrText = None
ldrbOn = False
backMenu = None
backTxt = None
myLdrbrd = list()   # The leaderboard is retrieved in a list


def leaderBoard():      # A leaderboard displaying the top
    global top1_name    # 5 players in game
    global top2_name
    global top3_name
    global top4_name
    global top5_name
    myLdrbrd = list()

    # Get the leaderboard from a text file
    with open('leaderboard.txt', 'r') as file:
        for line in file:
            player = list()
            for word in line.split():
                player.append(word)
            myLdrbrd.append(player)

    # Get coordinates
    x1 = sWidth / 2 - 300
    y1 = sHeight / 6 - 50
    x2 = x1 + 600
    y2 = y1 + 700

    # Display the data on canvas
    ldbrMenu = canvas.create_rectangle(x1, y1,
                                       x2, y2,
                                       fill="steel blue",
                                       outline="white")

    ldbrText = canvas.create_text((x1 + x2)/2,
                                  y1 + 50, fill="white",
                                  font="Times 50 bold",
                                  text="Leaderboard")
    txt1 = "1. "+str(myLdrbrd[0][1])+": "+str(myLdrbrd[0][0])
    top1_name = canvas.create_text((x1 + x2)/2,
                                   y1+150, fill="white",
                                   font="Times 20",
                                   text=txt1)
    txt2 = "2. "+str(myLdrbrd[1][1])+": "+str(myLdrbrd[1][0])
    top2_name = canvas.create_text((x1 + x2)/2,
                                   y1+250, fill="white",
                                   font="Times 20",
                                   text=txt2)
    txt3 = "3. "+str(myLdrbrd[2][1])+": "+str(myLdrbrd[2][0])
    top3_name = canvas.create_text((x1 + x2)/2,
                                   y1+350, fill="white",
                                   font="Times 20",
                                   text=txt3)
    txt4 = "4. "+str(myLdrbrd[3][1])+": "+str(myLdrbrd[3][0])
    top4_name = canvas.create_text((x1 + x2)/2,
                                   y1+450, fill="white",
                                   font="Times 20",
                                   text=txt4)
    txt5 = "5. "+str(myLdrbrd[4][1])+": "+str(myLdrbrd[4][0])
    top5_name = canvas.create_text((x1 + x2)/2,
                                   y1+550, fill="white",
                                   font="Times 20",
                                   text=txt5)

    # The back button to return to home page
    back_x1 = 50
    back_y1 = 50
    back_x2 = back_x1 + 200
    back_y2 = back_y1 + 50
    backMenu = canvas.create_rectangle(back_x1, back_y1,
                                       back_x2, back_y2,
                                       fill="steel blue",
                                       outline="white")
    backTxt = canvas.create_text((back_x1 + back_x2)/2,
                                 (back_y1 + back_y2)/2,
                                 fill="white", font="Times 20",
                                 text="Back")
    canvas.pack()
    return


def quitGame():     # A quit function
    window.quit()


def playAgain():    # Restores all the values
    global gameOver
    global score
    global level
    global countOn
    global canMaxChance
    global bagMaxChance
    global fishMaxChance
    global nextLevel

    if (not gameOver and not countOn):
        # Reset level and score
        level = 1
        score = 0

        # Reset the chances
        canMaxChance = 120
        fishMaxChance = 125
        bagMaxChance = 130
        nextLevel = 100

        # Clear all the lists of objects
        cans.clear()
        allFish.clear()
        bags.clear()
        bubbles.clear()

        # Clear everything on canvas and create it again
        canvas.delete("all")
        gameOver = False
        countOn = True
        startPoint()


def saveGame():     # Opens the file and saves the current values
    global level
    global canMaxChance
    global bagMaxChance
    global fishMaxChance
    global nextLevel
    global score
    global username

    # Save the level, score, username and the current chances
    # of creating objects (they vary accross different levels).
    savedgame = open("savedgame.txt", "w")
    savedgame.write(str(level) + "\n")
    savedgame.write(str(score) + "\n")
    savedgame.write(str(nextLevel) + "\n")
    savedgame.write(str(canMaxChance) + "\n")
    savedgame.write(str(fishMaxChance) + "\n")
    savedgame.write(str(bagMaxChance) + "\n")
    savedgame.write(str(username))
    savedgame.close()   # Close the file
    return


# ===================== Creating objects =======================
# Every object gets random y coordinate


def createCan():
    x_pos = sWidth + 50
    y_pos = randint(100, sHeight - 300)
    enemy = canvas.create_image(x_pos, y_pos, anchor=W, image=canImg)
    cans.append(enemy)
    return


def createFish():
    x_pos = sWidth + 50
    y_pos = randint(100, sHeight - 300)
    fish = canvas.create_image(x_pos, y_pos, anchor=W, image=fishImg)
    allFish.append(fish)
    return


def createBag():
    x_pos = sWidth + 50
    y_pos = randint(100, sHeight - 300)
    bag = canvas.create_image(x_pos, y_pos, anchor=W, image=bagImg)
    bags.append(bag)
    return


def createBubble():
    x_pos = randint(100, sWidth - 30)
    y_pos = sHeight + 10
    bubble = canvas.create_oval(x_pos, y_pos, x_pos + 10,
                                y_pos + 10, fill="steel blue")
    bubbles.append(bubble)
    return


# ===================== Light and dim objects ============================


def dimText(newScore):
    canvas.itemconfigure(scoreText, fill="white",
                         font="Times 20 italic", text=newScore)
    return


def lightText(newScore):    # The score gets orange when a fish has been eaten
    canvas.itemconfigure(scoreText, fill="orange",
                         font="Times 25 italic",  text=newScore)
    window.after(100, dimText, newScore)
    return


# =========== Move and collision detection functions =================


def moveObjects():  # Update the coordinates of every object on the canvas
    for i in range(len(cans)):
        canvas.move(cans[i], -8, 0)
    for i in range(len(allFish)):
        canvas.move(allFish[i], -10, 0)
    for i in range(len(bags)):
        canvas.move(bags[i], -6, 0)
    for i in range(len(bubbles)):
        canvas.move(bubbles[i], 0, -3)
    canvas.pack()   # Display changes


def objectHit():    # Colision detection function
    player = canvas.coords(mainObject)

    # Get player's coordinates
    x_pos1 = player[0]
    y_pos1 = player[1] - 10     # A hit is counted only if it is in the mouth
    x_pos2 = player[0] + 190    # area of the shark
    y_pos2 = player[1] + 25

    if (not noDeath):
        # Check if the player has hit a can
        for i in range(len(cans)):
            can = cans[i]
            x_can1 = canvas.coords(can)[0]
            y_can1 = canvas.coords(can)[1] - 30
            x_can2 = x_can1 + 48
            y_can2 = y_can1 + 59

            if (x_pos2 >= x_can1 and x_can1 >= x_pos2 - 15 and
                ((y_pos2 >= y_can1 and y_can2 >= y_pos1) or
                 (y_can2 >= y_pos1 and y_pos2 >= y_can1))):
                canvas.delete(cans[i])
                cans.remove(cans[i])
                return True

        # Check for collision with a plastic bag
        for i in range(len(bags)):
            bag = bags[i]
            x_bag1 = canvas.coords(bag)[0]
            y_bag1 = canvas.coords(bag)[1] - 30
            x_bag2 = x_bag1 + 48
            y_bag2 = y_bag1 + 59

            if (x_pos2 >= x_bag1 and x_bag1 >= x_pos2 - 15 and
                ((y_pos2 >= y_bag1 and y_bag2 >= y_pos1) or
                 (y_bag2 >= y_pos1 and y_pos2 >= y_bag1))):
                canvas.delete(bags[i])
                bags.remove(bags[i])
                return True

    # Check if the shark has eaten a fish
    for i in range(len(allFish)):
        fish = allFish[i]
        x_fish1 = canvas.coords(fish)[0]
        y_fish1 = canvas.coords(fish)[1] - 12
        x_fish2 = x_fish1 + 85
        y_fish2 = y_fish1 + 24

        if (x_pos2 >= x_fish1 and x_fish1 >= x_pos2 - 35 and
            ((y_pos2 >= y_fish1 and y_fish2 >= y_pos1) or
             (y_fish2 >= y_pos1 and y_pos2 >= y_fish1))):
            canvas.delete(allFish[i])
            allFish.remove(allFish[i])

            global score
            if (doubleScore):
                score += 20
            else:
                score += 10
            newScore = "Score: " + str(score)
            window.after(100, lightText, newScore)

            global nextLevel

            # The next level limit has been reached. Update it
            if (score >= nextLevel):
                nextLevel += 100

                global level
                level += 1  # New level! Display on canvas
                newLevel = "Level: " + str(level)
                canvas.itemconfigure(levelText, fill="white",
                                     font="Times 25 bold", text=newLevel)

                # ALso, update the chances (so it gets more challenging as
                # the user progresses through the game).
                global canMaxChance
                if (canMaxChance - 10 >= 35):
                    canMaxChance -= 10
                global bagMaxChance
                if (bagMaxChance - 10 >= 35):
                    bagMaxChance -= 10
                global fishMaxChance
                if (fishMaxChance - 10 >= 5):
                    fishMaxChance -= 10

            return False

    return False


# ==================== Coordinator functions =========================


def allocateMemory(checkCan, checkFish, checkBag, checkBubble):
    # When the objects leave the canvas, they should be deleted.
    # Otherwise, the program might crash (in case there is not enough RAM)
    if (checkCan):
        while (canvas.coords(cans[0])[0] <= -50):   # Check if out ou bounds
            canvas.delete(cans[0])
            cans.remove(cans[0])

    if (checkFish):
        while (canvas.coords(allFish[0])[0] <= -50):
            canvas.delete(allFish[0])
            allFish.remove(allFish[0])

    if (checkBag):
        while (canvas.coords(bags[0])[0] <= -50):
            canvas.delete(bags[0])
            bags.remove(bags[0])

    if (checkBubble):
        while (canvas.coords(bubbles[0])[1] <= -50):
            canvas.delete(bubbles[0])
            bubbles.remove(bubbles[0])
    return


def createMove():   # The main functions the coordinates the game
                    # (creating and moving the objects)

    # We check for the second cheat here
    canChance = randint(1, canMaxChance)
    if (not noObstacles):
        fishChance = randint(1, fishMaxChance)
    else:
        fishChance = randint(1, 35)
    bagChance = randint(1, bagMaxChance)
    bubbleChance = randint(1, 20)

    # Create objects on random intervals
    if (canChance == 1 and not noObstacles):
        createCan()
    if (fishChance == 2):
        createFish()
    if (bagChance == 3 and not noObstacles):
        createBag()
    if (bubbleChance == 4):
        createBubble()

    moveObjects()   # Move the objects created
    if (not noObstacles):
        allocateMemory(canChance == 1, fishChance == 2,
                       bagChance == 3, bubbleChance == 4)

    if (objectHit()):   # Check collision
        GameOver = canvas.create_text(sWidth / 2, sHeight / 2,
                                      fill="white", font="Times 50 bold",
                                      text="Game Over!")

        # In case we ate an unwanted object, we have to
        # update the leaderboard
        myLdrbrd = list()
        current = list()
        current.append(str(score))
        current.append(str(username))

        # Get the data in the array
        with open('leaderboard.txt', 'r') as file:
            for line in file:
                player = list()
                for word in line.split():
                    player.append(word)
                myLdrbrd.append(player)

        # If this is not a continuation, then just add the current
        # stats and sort the list again (in descending order)
        if (not loadedGame):
            myLdrbrd.append(current)
            for i in range(len(myLdrbrd) - 1):
                for j in range(i + 1, len(myLdrbrd)):
                    if (int(myLdrbrd[i][0]) < int(myLdrbrd[j][0])):
                        temp = myLdrbrd[i]
                        myLdrbrd[i] = myLdrbrd[j]
                        myLdrbrd[j] = temp

        else:   # Otherwise, find the player and update the score
            for i in range(len(myLdrbrd)):
                if (myLdrbrd[i][1] == str(username)):
                    myLdrbrd[i][0] = str(score)
                    for i in range(len(myLdrbrd) - 1):
                        for j in range(i + 1, len(myLdrbrd)):
                            if (int(myLdrbrd[i][0]) < int(myLdrbrd[j][0])):
                                temp = myLdrbrd[i]
                                myLdrbrd[i] = myLdrbrd[j]
                                myLdrbrd[j] = temp
                    break

        # Save the list in the file
        with open('leaderboard.txt', 'w') as file:
            for i in range(len(myLdrbrd)):
                file.write(myLdrbrd[i][0] + " " + myLdrbrd[i][1] + "\n")

        global gameOver
        global gameOn
        gameOver = True
        gameOn = False
        createOptions()
        return

    # Loop again in pause button is not pressed
    if (not pause):
        global canGo
        canGo = True
        window.after(30, createMove)


# ================= Initialize the canvas and countdown ======================


def countdown(counter):     # Counting 3, 2, 1, Go so the player gets ready
    global Counting
    global canGo
    global countOn
    canGo = False
    if (counter == 3):
        Counting = canvas.create_text(sWidth / 2, sHeight / 2,
                                      fill="white",
                                      font="Times 30 bold",
                                      text=str(3))
    if (counter >= 1):
        canvas.itemconfigure(Counting, text=str(counter))
    else:
        canvas.itemconfigure(Counting, text="Go!")
    if (counter < 0):   # Counting has finished, return
        canvas.delete(Counting)
        countOn = False
        return
    canvas.pack()
    if (countOn):
        window.after(1000, countdown, counter - 1)


def startPoint():       # Delete the menus and display
    global startMenu    # the main object
    global loadMenu
    global leaderboardMenu
    global quitMenu
    global startText
    global loadText
    global leaderboardText
    global quitText
    global gameOn
    global againMenu
    global againText
    global mainMenu
    global mainText
    global userNameText
    global username
    global menusOn
    global countOn
    global gameOver

    # Remove all the text and menus
    gameOn = True
    menusOn = False
    countOn = True
    gameOver = False
    canvas.delete(startMenu)
    canvas.delete(startText)
    canvas.delete(loadMenu)
    canvas.delete(loadText)
    canvas.delete(leaderboardMenu)
    canvas.delete(leaderboardText)
    canvas.delete(quitMenu)
    canvas.delete(quitText)
    canvas.delete(againMenu)
    canvas.delete(againText)
    canvas.delete(mainMenu)
    canvas.delete(mainText)

    # Get globals
    global mainObject
    global sWidth
    global sHeight
    global canStart

    # Set background
    canvas.create_image(sWidth/2, sHeight, image=background, anchor=S)

    # Create and place the main object
    mainObject = canvas.create_image(0, 0, anchor=W,
                                     image=sharkImg)
    canvas.move(mainObject, sWidth / 3, sHeight / 2)

    # Display the score
    global scoreText
    global levelText
    scoreText = canvas.create_text(sWidth - 70, 30, fill="white",
                                   font="Times 20 italic",
                                   text="Score: "+str(score))
    levelText = canvas.create_text(100, 30, fill="white",
                                   font="Times 25 bold",
                                   text="Level: "+str(level))
    userNameText = canvas.create_text(sWidth/2, 30, fill="white",
                                      font="Times 20 bold",
                                      text=str(username))
    canvas.pack()
    countdown(3)
    window.after(4000, createMove)
    return


# =============== Creating menus and options ==================


def createOptions():    # Create options after a game over
    global againText
    global mainText
    global againMenu
    global mainMenu
    global pause
    pause = False

    # Play again option: coordinates and menu
    again_x1 = (sWidth / 3) - 150
    again_y1 = 2*(sHeight / 3) - 30
    again_x2 = again_x1 + 300
    again_y2 = again_y1 + 60

    againMenu = canvas.create_rectangle(again_x1, again_y1,
                                        again_x2, again_y2,
                                        fill="steel blue",
                                        outline="white")
    againText = canvas.create_text((again_x1 + again_x2)/2,
                                   (again_y1 + again_y2)/2,
                                   fill="white",
                                   font="Times 20 bold",
                                   text="Play again?")

    # Back to main menu: coordinates and menu
    main_x1 = 2*(sWidth/3) - 150
    main_y1 = 2*(sHeight / 3) - 30
    main_x2 = main_x1 + 300
    main_y2 = main_y1 + 60

    mainMenu = canvas.create_rectangle(main_x1, main_y1,
                                       main_x2, main_y2,
                                       fill="steel blue",
                                       outline="white")
    mainText = canvas.create_text((main_x1 + main_x2)/2,
                                  (main_y1 + main_y2)/2,
                                  fill="white",
                                  font="Times 20 bold",
                                  text="Return to home page")
    canvas.pack()
    return


def menuPage():                 # Creating the main menu page
    global startMenu
    global loadMenu
    global leaderboardMenu
    global quitMenu
    global startText
    global loadText
    global leaderboardText
    global quitText
    global gameOn
    global pause
    global menusOn
    menusOn = True
    gameOn = False
    pause = False

    # Set background
    canvas.create_image(sWidth/2, sHeight, image=background, anchor=S)

    # Start menu
    start_x1 = sWidth / 2 - 300
    start_y1 = sHeight / 4 - 50
    start_x2 = start_x1 + 600
    start_y2 = start_y1 + 100
    startMenu = canvas.create_rectangle(start_x1, start_y1,
                                        start_x2, start_y2,
                                        fill="steel blue",
                                        outline="white")
    startText = canvas.create_text((start_x2 + start_x1)/2,
                                   (start_y2 + start_y1)/2,
                                   fill="white",
                                   font="Times 30 bold",
                                   text="Start new game")

    # Load menu
    load_x1 = start_x1
    load_y1 = start_y2 + 40
    load_x2 = start_x2
    load_y2 = load_y1 + 100
    loadMenu = canvas.create_rectangle(load_x1, load_y1,
                                       load_x2, load_y2,
                                       fill="steel blue",
                                       outline="white")
    loadText = canvas.create_text((load_x2 + load_x1)/2,
                                  (load_y2 + load_y1)/2,
                                  fill="white", font="Times 30 bold",
                                  text="Load last saved game")

    # Leaderboard menu
    ldr_x1 = start_x1
    ldr_y1 = load_y2 + 40
    ldr_x2 = start_x2
    ldr_y2 = ldr_y1 + 100
    leaderboardMenu = canvas.create_rectangle(ldr_x1, ldr_y1,
                                              ldr_x2, ldr_y2,
                                              fill="steel blue",
                                              outline="white")
    leaderboardText = canvas.create_text((ldr_x1 + ldr_x2)/2,
                                         (ldr_y1 + ldr_y2)/2,
                                         fill="white",
                                         font="Times 30 bold",
                                         text="Leaderboard")

    # Quit menu
    quit_x1 = start_x1
    quit_y1 = ldr_y2 + 40
    quit_x2 = start_x2
    quit_y2 = quit_y1 + 100
    quitMenu = canvas.create_rectangle(quit_x1, quit_y1,
                                       quit_x2, quit_y2,
                                       fill="steel blue",
                                       outline="white")
    quitText = canvas.create_text((quit_x2 + quit_x1)/2,
                                  (quit_y1 + quit_y2)/2,
                                  fill="white",
                                  font="Times 30 bold",
                                  text="Quit")
    canvas.pack()
    return


# ================= Main ===========================


window = Tk()
window.title("Dodging Game")
window.overrideredirect(True)
window.overrideredirect(False)
window.attributes("-fullscreen", True)

# Window size
sWidth = window.winfo_screenwidth()
sHeight = window.winfo_screenheight()

# Create a black background
canvas = Canvas(window, bg="black", width=sWidth, height=sHeight)
# pack the canvas into a frame/form
canvas.pack(expand=YES, fill=BOTH)
background = PhotoImage(file='oceanResize.png')

# Get the images
sharkImg = PhotoImage(file='sharkS.png')
canImg = PhotoImage(file='canS.png')
fishImg = PhotoImage(file='fishS.png')
bagImg = PhotoImage(file='bagS.png')
screenshotImg = PhotoImage(file='screenshot.png')

# Bind the keys
canvas.bind("<Left>", leftKey)
canvas.bind("<Right>", rightKey)
canvas.bind("<Up>", upKey)
canvas.bind("<Down>", downKey)
canvas.bind("<n><o><d><e><a><t><h>", cheatKey)
canvas.bind("<Escape>", pauseKey)
canvas.bind("<e><x><i><t>", exitKey)
canvas.bind("<Return>", bossKey)
canvas.bind("<d><o><u><b><l><e>", cheatKey2)
canvas.bind("<n><o><o><b><j><e><c><t>", cheatKey3)
canvas.bind("<Button-1>", clickEvent)
canvas.focus_set()

countOn = True
menuPage()
window.mainloop()
