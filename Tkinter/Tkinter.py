import tkinter
from tkinter import *
Win = Tk()
Win.geometry("1000x600")
def eexit():
    Win.destroy()
    exit()
testbutton = Button(Win,text="exit",width=10,command=eexit,bg="red")
testbutton.place(y = 500, x = 300)

Win.mainloop()