from tkinter import *
from tkinter import font
import packages.functions

packages.functions.login()
packages.functions.master_lists()

### WINDOW ###

window=Tk()

# Canvas
canvas1=Canvas()
canvas1.config(width='1280', height='720')
line1=canvas1.create_line(290,60,290,720,fill='#458588',width=2, dash = (2,5))
line2 = canvas1.create_line(870, 60, 870, 720, fill = '#458588', width = 2, dash = (2,5))
line3 = canvas1.create_line(0,60,1280,60, fill = '#fb4934', width = 3)
canvas1.pack()

# Set Window Configurations
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Tw Cen MT", size=13)
window.title('Editor')
window.geometry("1280x720")
window.tk_setPalette(background="#282828", foreground="#ebdbb2")
bg = "#282828"
fg = "#ebdbb2"
graybox = "#a89984"
### WIDGETS ###

# Title
Topic = Label(window, text="Student Marksheet", fg = "#b8bb26", font = ("Bahnschrift",30))
Topic.place(x=475,y=29)

# Headers
acad_lbl = Label(window, text="Academic Data", font=("Bahnschrift",20))
acad_lbl.place(x=480, y=125)
Input_Marks_lbl = Label(window, text="Enter Marks:", font=("Bahnschrift",20))
Input_Marks_lbl.place(x=960, y=125)

# Student Info
Data_lbl = Label(window, text="Student Data", font = ("Bahnschrift",20))
Data_lbl.place(x = 60, y = 125) 

FirstNam_lbl = Label(window, text = "First Name")
FirstNam_lbl.place(x = 30, y = 200)
FirstNam_txt = Entry(window, bd = 2, selectbackground=fg, selectforeground=bg)
FirstNam_txt.place(x = 130, y = 200)

LastNam_lbl = Label(window, text = "Last Name")
LastNam_lbl.place(x=30 , y=250 )
LastNam_txt = Entry(window, bd = 2, selectbackground=fg, selectforeground=bg)
LastNam_txt.place(x = 130, y = 250 )

Roll_lbl = Label(window, text = "Roll No.")
Roll_lbl.place(x = 30, y = 300)
Roll_txt = Entry(window, bd =2, selectbackground=fg, selectforeground=bg)
Roll_txt.place(x = 130, y = 300)

Adm_lbl = Label(window, text = "Admission No.")
Adm_lbl.place(x = 30, y = 350)
Adm_txt = Entry(window, bd = 2, selectbackground=fg, selectforeground=bg)
Adm_txt.place(x = 130, y = 350)

# Class and Section Selection

Standard = Label(window, text = "Class")
Standard.place(x = 30, y = 423)
Section = Label(window, text = "Section")
Section.place(x = 130, y = 423)

clicked1= StringVar()
clicked1.set("")

clicked2 = StringVar()
clicked2.set("")

drop1 = OptionMenu(window, clicked1, *packages.functions.classlist)
drop1.place(x = 70, y =420)

drop2 = OptionMenu(window, clicked2, *packages.functions.sectionlist)
drop2.place(x = 185, y= 420)

# Gender-selection (yes there are only 2 genders boohooo)
gendervar = StringVar()
gendervar.set(' ')

Gender_lbl = Label(window, text = "Gender")
Gender_lbl.place(x = 30, y = 513)
Male = Radiobutton(window, text ="Male",variable = gendervar, value = "Male", selectcolor = bg)
Male.place(x = 90, y = 500)

Female = Radiobutton(window, text = "Female",variable = gendervar, value = "Female", selectcolor = bg)
Female.place(x = 90, y = 525)

# Subject-wise marks input

subvar = StringVar()
subvar.set("None")

subject_drop = OptionMenu(window, subvar, *packages.functions.sublist)
subject_drop.place(x=390,y=200)

sub_lbl = Label(window, text="Subject")
sub_lbl.place(x=330,y=203)

exam_lbl = Label(window, text="Exam Name")
exam_lbl.place(x=575,y=203)

exam_text = Entry(window)
exam_text.place(x=675,y=206)

marks_lbl = Label(window, text="Marks")
marks_lbl.place(x=330,y=250)

marks_obt = Entry(window, width=3)
marks_obt.place(x=390,y=254)

slash_lbl = Label(window, text='/', font=('Bahnschrift', 23))
slash_lbl.place(x=420,y=240)

total_mks = Entry(window, width=3)
total_mks.place(x=445,y=254)

date_lbl = Label(window, text="Date")
date_lbl.place(x=575, y=250)

date_text = StringVar()
date_text.set("YYYY-MM-DD")
date_inp = Entry(window, textvariable=date_text)
date_inp.place(x=675,y=253 )

submit_btn = Button(window, text = "Submit", command = packages.functions.getmarks)
window.mainloop()
