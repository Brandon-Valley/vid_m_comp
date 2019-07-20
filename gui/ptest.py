from tkinter import *

master = Tk()

leftValue = IntVar()  # IntVars to hold
rightValue = IntVar() # values of scales

leftScale = Scale(master, from_=0, to=249, variable=leftValue, showvalue=0)
leftScale.set(152)

rightScale = Scale(master, from_=0, to=249, variable=rightValue, showvalue=0)
rightScale.set(152)

leftLabel = Label(master, textvariable=leftValue)   # labels that will update
rightLabel = Label(master, textvariable=rightValue) # with IntVars as slider moves

leftLabel.grid(row=0, column=0)
leftScale.grid(row=0, column=1)
rightLabel.grid(row=0, column=3)
rightScale.grid(row=0, column=2)

mainloop()
