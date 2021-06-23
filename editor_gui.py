import tkinter as tk
from tkinter import font
from tkinter import*


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
Topic.place(x=475,y=29)

# Student Personal Info
Data_lbl = tk.Label(window, text="Student Data:", font = ("Bahnschrift",20))
Data_lbl.place(x = 60, y = 125) 

FirstNam_lbl = tk.Label(window, text = "First Name")
FirstNam_lbl.place(x = 30, y = 200)
FirstNam_txt = tk.Entry(window, bd = 2)
FirstNam_txt.place(x = 120, y = 200)

LastNam_lbl = tk.Label(window, text = "Last Name")
LastNam_lbl.place(x=30 , y=250 )
LastNam_txt = tk.Entry(window, bd = 2)
LastNam_txt.place(x = 120, y = 250 )

Roll_lbl = tk.Label(window, text = "Roll No.")
Roll_lbl.place(x = 30, y = 300)
Roll_txt = tk.Entry(window, bd =2)
Roll_txt.place(x = 98, y = 300)

Adm_lbl = tk.Label(window, text = "Admission No.")
Adm_lbl.place(x = 30, y = 350)
Adm_txt = tk.Entry(window, bd = 2)
Adm_txt.place(x = 136, y = 350)

#RadioButton
var = StringVar()
var.set(' ')

Gender_lbl = tk.Label(window, text = "Gender")
Gender_lbl.place(x = 30, y = 510)
Male = Radiobutton(window, text ="Male",variable = var, value = 1, selectcolor= "black")
Male.place(x = 90, y = 500)

Female = Radiobutton(window, text = "Female",variable = var, value = 2, selectcolor = "black")
Female.place(x = 90, y = 520)

# Header
marks_lbl = tk.Label(window, text="Academic Data:", font=("Bahnschrift",20))
marks_lbl.place(x=380, y=125)

# Subject-wise CheckButtons

Selectedsub_frame = LabelFrame(window, text = "Subjects studying", font = ("Times New Roman", 17))
Selectedsub_frame.place(x = 350, y = 200,width= 250, height = 240)

Phy, Che, Mat, Bio, His, Civ, Geo, Eco, Hin, Eng = IntVar(),IntVar(),IntVar(),IntVar(),IntVar(), \
IntVar(),IntVar(),IntVar(),IntVar(),IntVar()

Phy_Check = Checkbutton(Selectedsub_frame, text = "Physics", variable=Phy, onvalue=1, offvalue=0, selectcolor="black")
Phy_Check.place(x = 2, y= 0)
Che_Check = Checkbutton(Selectedsub_frame, text = "Chemistry", variable=Che, onvalue=1, offvalue=0, selectcolor="black")
Che_Check.place(x = 2, y= 40)
Mat_Check = Checkbutton(Selectedsub_frame, text = "Maths", variable=Mat, onvalue=1, offvalue=0, selectcolor="black")
Mat_Check.place(x = 2, y= 80)
Bio_Check = Checkbutton(Selectedsub_frame, text = "Biology", variable=Bio, onvalue=1, offvalue=0, selectcolor="black")
Bio_Check.place(x = 2, y= 120)
His_Check = Checkbutton(Selectedsub_frame, text = "History", variable=His, onvalue=1, offvalue=0, selectcolor="black")
His_Check.place(x = 2, y= 160)
Civ_Check = Checkbutton(Selectedsub_frame, text = "Civics", variable=Civ, onvalue=1, offvalue=0, selectcolor="black")
Civ_Check.place(x = 130, y= 0)
Geo_Check = Checkbutton(Selectedsub_frame, text = "Geography", variable=Geo, onvalue=1, offvalue=0, selectcolor="black")
Geo_Check.place(x = 130, y= 40)
Eco_Check = Checkbutton(Selectedsub_frame, text = "Economics", variable=Eco, onvalue=1, offvalue=0, selectcolor="black")
Eco_Check.place(x = 130, y= 80)
Hin_Check = Checkbutton(Selectedsub_frame, text = "Hindi", variable=Hin, onvalue=1, offvalue=0, selectcolor="black")
Hin_Check.place(x = 130, y= 120)
Eng_Check = Checkbutton(Selectedsub_frame, text = "English", variable=Eng, onvalue=1, offvalue=0, selectcolor="black")
Eng_Check.place(x = 130, y= 160)


#Drop-Down Menu

Standard = Label(window, text = "Standard", font = ("Times New Roman", 13))
Standard.place(x = 20, y = 420)
Section = Label(window, text = "Section", font = ("Times New Roman", 13))
Section.place(x = 150, y = 420)

options1 = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
options2 = ['A','B','C','D','E','F','G','H','I','J','K']

clicked1= StringVar()
clicked1.set("")

clicked2 = StringVar()
clicked2.set("")

drop1 = OptionMenu(window, clicked1, *options1)
drop1.place(x = 86, y =420)

drop2 = OptionMenu(window, clicked2, *options2)
drop2.place(x = 210, y= 420)


window.mainloop()


