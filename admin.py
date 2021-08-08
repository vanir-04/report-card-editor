from tkinter import *
from tkinter import ttk
from tkinter import font
import os

window = Tk()

cwd = os.path.dirname(os.path.abspath(__file__))

defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Tw Cen MT", size=13)
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Tw Cen MT", size=13)
window.title('Admin')
window.iconbitmap(os.path.join(cwd,'assets/admin.ico'))
window.geometry("800x450")
window.tk_setPalette(background="#282828", foreground="#ebdbb2")
window.resizable(0, 0)
bg = "#282828"
fg = "#ebdbb2"
graybox = "#a89984"

title = Label(window, text="Admin Mode", fg = "#b8bb26", font = ("Bahnschrift",30))
title.place(relx=0.5, rely=0.1, anchor=CENTER)

school = Label(window, text="School", fg=fg)

window.mainloop()