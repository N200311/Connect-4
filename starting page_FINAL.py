from os import startfile
import tkinter as tk
from tkinter import *

HEIGHT = 500
WIDTH = 600

root = tk.Tk() #to make the window
root.title('CONNECT 4')

#used in your application to draw forms like as lines, ovals, polygons, and rectangles.
canvas = Canvas(root, height=HEIGHT, width=WIDTH)
#Before installing widgets in the parent widget, this geometry manager divides them into blocks.
canvas.pack()

#adding a frame to the root window
frame1 = Frame(root, bg='#cce6ff')
frame1.place(relwidth=1, relheight=1)

#adding a frame to the root window
frame2 = Frame(root, bg='#1a90ff', bd=5)
frame2.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

#adding a label to the root window
label1 = Label(frame2, text='WELCOME TO OUR CONNECT 4 GAME', bg='#1a90ff', fg='white', font='bold')
label1.place(relwidth=1, relheight=1)

#adding a frame to the root window
frame3 = Frame(root, bg='#1a90ff', bd=10)
frame3.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

#adding a label to the root window
label2 = Label(frame3, text='HOW MANY PLAYERS:', bg='#1a90ff', fg='white', font='bold')
label2.place(relwidth=1, relheight=0.25, )

#To call the 1V1 game using a button
def call_1V1(): 
    startfile('first draft 1 VS 1_FINAL.py')

button1 = tk.Button(frame3,text='TWO PLAYERS',command=call_1V1, bg='#99b3ff',font='bold')
button1.place(relwidth=0.5, relheight=0.2, relx=0.25, rely=0.3)

#to call the AI game using a button
def call_AI():
    startfile('First Draft AI_FINAL.py')

button2 = tk.Button(frame3,text='ONE PLAYER',command=call_AI, bg='#99b3ff',font='bold')
button2.place(relwidth=0.5, relheight=0.2, relx=0.25, rely=0.6)


root.mainloop()#to make the window run