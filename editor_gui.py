import tkinter as tk
from tkinter import font

window=tk.Tk()

# Canvas
canvas1=tk.Canvas()
canvas1.config(width='1280', height='720')
line1=canvas1.create_line(290,60,290,720,fill='#458588',width=2, dash = (2,5))
line2 = canvas1.create_line(0,60,1280,60, fill = '#fb4934', width = 3)
canvas1.pack()

# Set Window Configurations
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Noto Sans", size=11)
window.title('Editor')
window.geometry("1280x720")
window.tk_setPalette(background="#282828", foreground="#ebdbb2")

### WIDGETS ###

# Title
Topic = tk.Label(window, text="Student Marksheet", fg = "#b8bb26", font = ("Bahnschrift",30))
Topic.place(x=500,y=10)

# Name field
Nam_lbl = tk.Label(window, text="Student Name", font = ("Bahnschrift",15))
Nam_lbl.place(x = 82, y = 105) 

Nam_txt = tk.Entry(window, bd = 2)
Nam_txt.place(x = 60, y = 130)

# Header
marks_lbl = tk.Label(window, text="Marks scored in:", font=("Bahnschrift",20))
marks_lbl.place(x=380, y=125)

# Subject-wise
Phy_lbl = tk.Label(window, text ="Physics")
Phy_lbl.place(x=520,y=200)

Che_lbl = tk.Label(window, text ="Chemistry")
Che_lbl.place(x=520,y=250)

Mat_lbl = tk.Label(window, text ="Maths")
Mat_lbl.place(x=520,y=300)

Cs_lbl =  tk.Label(window, text ="CS")
Cs_lbl.place(x=520,y=350)

Eng_lbl = tk.Label(window, text ="English")
Eng_lbl.place(x=520,y=400)


# Inputs for each subject
Phy_txt = tk.Entry(window, bd = 2)
Phy_txt.place(x=610, y = 200)

Che_txt = tk.Entry(window, bd = 2)
Che_txt.place(x=610, y = 250)

Mat_txt = tk.Entry(window, bd = 2)
Mat_txt.place(x=610, y = 300)

Cs_txt = tk.Entry(window, bd = 2)
Cs_txt.place(x=610, y = 350)

Eng_txt = tk.Entry(window, bd = 2)
Eng_txt.place(x=610, y = 400)


window.mainloop()


