__author__  = "Emily Sheehan"
__version__ = 1.0

import tkinter as tk
import random
import math
import Pmw

"""Welcome to my Circle Game Project. This project uses a Tkinter user interface.
   The purpose of this game is to click as close to the center of the randomly
   placed circles as possible. The goal is to end the game with the highest score!"""

root = tk.Tk()
root.title("Welcome to Emily's Project")

w = 900
h = 900
x = 20
y = 20

root.geometry('%dx%d+%d+%d' % (w, h, x, y))
canvasBig = tk.Canvas()
canvasBig.pack(pady=100)
canvasBig.config(bg="black", width=700, height=700)

balloon = Pmw.Balloon(root) #Appears when you hover over title

welcome = tk.Label(root, fg="darkblue", text="Welcome to Circle Game!", font= "Symbol 36 bold")
welcome.place(x=225, y=50)
balloon.bind(welcome, "Instructions: Click as close to the center of the circles below!")

score = tk.IntVar(root) #variable that when changed, will change in label
score.set(100) # you change it's value by calling .set

scoreL = tk.Label(root, bg="#F203C7", fg="#14C6ED", text="Score: ", font = "Symbol 16 bold italic")
scoreL.place(x=360, y=710)

label = tk.Label(root, bg="#F203C7", fg="#14C6ED", textvariable=(score), font = "Symbol 16 bold italic")
label.place(x=425, y=710)

#Various lists that are used to calculate distance from click to circle center.
oval_coords = []
all_ovals = []
circle_centers = []
radii = []

def drawCircles():
    """
    Draws 10 circles in random locations on the board.
        
    Arguments-
    :none: 
        
    Return-
    :none:
    """       
    for i in range(10):
        top_x    = random.randint(50,600)
        top_y    = random.randint(50,600)
        size     = random.randint(10,100)
        bottom_x = top_x + size
        bottom_y = top_y + size
        
        canvasBig.oval = canvasBig.create_oval(top_x, top_y, bottom_x, bottom_y, fill="#14C6ED")
        all_ovals.append(canvasBig.oval)
        
        #gets center coordinate
        avg_x = int((top_x + bottom_x)/2) 
        avg_y = int((top_y + bottom_y)/2)
        
        radius = (bottom_x - top_x)/2
        radii.append(radius)
        circle_centers.append([avg_x, avg_y])

clicks = 0
def clicked(event):
    """
    Called on mouse press. Gets coordinate of click,
    and calls get_score.
        
    Arguments-
    :event: the mouseclick
        
    Return-
    :none:
    """       
    global clicks
    
    xloc = event.x
    yloc = event.y
    clicks +=1
    get_score(xloc, yloc)

def get_circle(event):
    """
    Gets location of mouse on drag, calls find_if_in_circle.
        
    Arguments-
    :event: mouse loc on drag
        
    Return-
    :none:
    """       
    currentxLoc = event.x
    currentyLoc = event.y

    find_if_in_circle(currentxLoc, currentyLoc)

def find_if_in_circle(x, y):
    """
    This function figures out if the mouse is hovering
    over a circle. If it is, it highlights the circle pink.
        
    Arguments-
    :x: current x-coord on drag
    :y: current y-coord on drag
    
    Return-
    :none:
    """   
    
    for circle in range(len(all_ovals)):
        center       = circle_centers[circle]
        radius       = radii[circle]
        x_dist = x - center[0]
        y_dist = y - center[1]
        
        distance = math.sqrt((x_dist**2) + (y_dist**2)) #distance formula
        
        if distance < radius:
            canvasBig.oval = all_ovals[circle]
            canvasBig.itemconfig(canvasBig.oval, fill="#F203C7")
            circle_chosen = circle
    
        if distance > radius:
            canvasBig.oval = all_ovals[circle]
            canvasBig.itemconfig(canvasBig.oval, fill="#14C6ED")

def get_score(x,y):
    """
    Called in clicked. Calculates score based off of distance between
    "click" and the center of the circle.
        
    Arguments-
    :x: x coord of click
    :y": y coord of click
        
    Return-
    :none:
    """   
    global score
    global clicks
    global add_name
    
    for circle in range(len(all_ovals)):
        
        center       = circle_centers[circle]
        radius       = radii[circle]
        x_dist = x - center[0]
        y_dist = y - center[1]
        
        distance = int(math.sqrt((x_dist**2) + (y_dist**2))) #distance formula
        
        if distance < radius: #if inside circle
            score.set(score.get() - distance) 
            
            if score.get() <= 0 or clicks == 10: 
                canvasBig.delete("all")
                canvasBig.create_text(350,350,fill="#F203C7", font="Symbol 40 italic bold",
                                        text="GAME OVER.")
                add_name = tk.Button(root, text ="View Leaderboard", command=enterScore)
                add_name.place(x=385, y=750)

            canvasBig.delete(all_ovals[circle]) #deletes clicked circle from canvas
            
        else:
            pass

def enterScore():
    """
    Takes user's score and asks for their name.
    Calls getAndAddScores.
        
    Arguments-
    :none: 
        
    Return-
    :none:
    """   
    
    global e 
    global add_name
    
    add_name.destroy()
    e = tk.Entry(root, text="Enter Your Name Here")
    e.place(x=350, y=750)
    name = e.get()
    final_score = score.get()
    
    addYourScore = tk.Button(root, text ="Add My Score", command=lambda: getAndAddScores(final_score))
    addYourScore.place(x=400, y=775)
      
    
def getAndAddScores(score):
    """
    Gets user score and name. Adds to txt file.
    Then, gets all name and scores from txt file and adds
    to list.
        
    Arguments-
    :score: user's score
        
    Return-
    :none:
    """       
    global e
    all_scores = []
    name = e.get()
    with open("highscores.txt", "a") as f:
        f.write(name + ": " + str(score))
        f.write("\n")        
        
    f = open("highscores.txt",'r')
    
    for line in f:
        name_and_score = line.split(":")
        name = name_and_score[0]
        score = name_and_score[1]
        all_scores.append([name, score])
    
    all_scores.sort() #sorts alphabetically
    showScores(all_scores)        
    
def showScores(all_scores):
    """
    Displays all scores in a new window.
        
    Arguments-
    :all_scores: all the previous scores from the txt file
        
    Return-
    :none:
    """   
    
    leaderboard = tk.Tk()
    leaderboard.geometry('%dx%d+%d+%d' % (200, 400, 5, 5))
    
    l = tk.Label(leaderboard, text="SCOREBOARD", font="Symbol 25 bold italic")
    l.pack(side="top")

    for i in range(len(all_scores)):
        NameAndScore = all_scores[i][0] + ": " + all_scores[i][1]
        tk.Label(leaderboard, text=NameAndScore, font="Symbol 15 bold italic").pack()    

canvasBig.bind("<Button-1>", clicked)
drawCircles()
canvasBig.bind("<Motion>", get_circle)    
root.mainloop()