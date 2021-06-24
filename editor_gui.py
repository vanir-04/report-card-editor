import tkinter as tk
from tkinter import font
from tkinter import*
import tkinter


window=tk.Tk()

# Canvas
canvas1=tk.Canvas()
canvas1.config(width='1280', height='720')
line1=canvas1.create_line(290,60,290,720,fill='#458588',width=2, dash = (2,5))
line2 = canvas1.create_line(0,60,1280,60, fill = '#fb4934', width = 3)
line3 = canvas1.create_line(870, 60, 870, 720, fill = '#458588', width = 2, dash = (2,5))
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

#Streams and Optionals
var1 = IntVar()
var1.set(' ') 


# Subject-wise CheckButons



Selectedsub_frame = LabelFrame(window, text = "Subjects studying", font = ("Times New Roman", 17))
Selectedsub_frame.place(x = 350, y = 200,width= 190, height = 250)

Science_Math = Radiobutton(Selectedsub_frame, text = "PCM", variable=var1, value = 1, selectcolor="black")
Science_Math.place(x = 2, y= 0)
Science_Bio = Radiobutton(Selectedsub_frame, text = "PCB", variable=var1, value = 2, selectcolor="black")
Science_Bio.place(x = 2, y= 40)
Science_Math_Bio = Radiobutton(Selectedsub_frame, text = "PCMB", variable=var1, value = 3, selectcolor="black")
Science_Math_Bio.place(x = 2, y= 80)
Humanity = Radiobutton(Selectedsub_frame, text = "Humanities", variable=var1, value = 4, selectcolor="black")
Humanity.place(x = 2, y= 120)
Comm = Radiobutton(Selectedsub_frame, text = "Commerce", variable=var1,value = 5, selectcolor="black")
Comm.place(x = 2, y = 160)


#Optional Subject Chosen
Optional_Frame = LabelFrame(window, text = "Optional Subject", font = ("Times New Roman", 17))
Optional_Frame.place(x = 600, y = 200, width = 200, height = 220)




var2 = IntVar()
var2.set(' ')

Comp_Radiobutton = Radiobutton( text = "Computer Sc.", variable=var2, value = 1, selectcolor="black")
Sports_Radiobutton = Radiobutton( text = "Physical Ed.", variable=var2, value = 2, selectcolor="black")
Psy_Radiobutton = Radiobutton( text = "Psychology", variable=var2, value = 3, selectcolor="black")
Eco_Radiobutton = Radiobutton( text = "Economics", variable=var2, value = 4, selectcolor="black")
Biotech_Radiobutton = Radiobutton( text = "BioTech", variable=var2, value = 3, selectcolor="black")
Mat_Radiobutton = Radiobutton( text = "Maths", variable=var2, value = 1, selectcolor="black")

#Defining Optional_Button
def Optional_Selection():
    if var1.get() == 1:
        Comp_Radiobutton = Radiobutton(Optional_Frame, text = "Computer Sc.", variable=var2, value = 1, selectcolor="black")
        Comp_Radiobutton.pack()
        Sports_Radiobutton = Radiobutton(Optional_Frame, text = "Physical Ed.", variable=var2, value = 2, selectcolor="black")
        Sports_Radiobutton.pack()
        Psy_Radiobutton = Radiobutton(Optional_Frame, text = "Psychology", variable=var2, value = 3, selectcolor="black")
        Psy_Radiobutton.pack()
        Eco_Radiobutton = Radiobutton(Optional_Frame, text = "Economics", variable=var2, value = 4, selectcolor="black")
        Eco_Radiobutton.pack()
    elif var1.get() == 2:
        Sports_Radiobutton = Radiobutton(Optional_Frame, text = "Physical Ed.", variable=var2, value = 1, selectcolor="black")
        Sports_Radiobutton.pack()
        Psy_Radiobutton = Radiobutton(Optional_Frame, text = "Psychology", variable=var2, value = 2, selectcolor="black")
        Psy_Radiobutton.pack()
        Biotech_Radiobutton = Radiobutton(Optional_Frame, text = "BioTech", variable=var2, value = 3, selectcolor="black")
        Biotech_Radiobutton.pack()
        Eco_Radiobutton = Radiobutton(Optional_Frame, text = "Economics", variable=var2, value = 4, selectcolor="black")
        Eco_Radiobutton.pack()
    elif var1.get() == 3:
        No_Optional_lbl = Label(Optional_Frame, text = "No Optional Subjects \n for PCMB", font = ('Times New Roman', 13))
        No_Optional_lbl.place(x = 15, y = 70)
    elif var1.get() == 4:
        Mat_Radiobutton = Radiobutton(Optional_Frame, text = "Maths", variable=var2, value = 1, selectcolor="black")
        Mat_Radiobutton.pack()
        Sports_Radiobutton = Radiobutton(Optional_Frame, text = "Physical Ed.", variable=var2, value = 2, selectcolor="black")
        Sports_Radiobutton.pack()
    elif var1.get() == 5:
        Comp_Radiobutton = Radiobutton(Optional_Frame, text = "Computer Sc.", variable=var2, value = 3, selectcolor="black")
        Comp_Radiobutton.pack()
        Sports_Radiobutton = Radiobutton(Optional_Frame, text = "Physical Ed.", variable=var2, value = 4, selectcolor="black")
        Sports_Radiobutton.pack()
        Psy_Radiobutton = Radiobutton(Optional_Frame, text = "Psychology", variable=var2, value = 5, selectcolor="black")
        Psy_Radiobutton.pack()

        


#Cmd_Function
Cmd_Btn = Button(text = "Select Optional Subjects", bg = 'black', command = Optional_Selection)
Cmd_Btn.place(x = 450, y = 480)  


#Reset Button
def reset():
    var.set(' ')
    var1.set(' ')
    var2.set(' ')
    FirstNam_txt.delete(0, END)
    LastNam_txt.delete(0, END)
    Adm_txt.delete(0, END)
    Roll_txt.delete(0, END)
    clicked1.set('')
    clicked2.set('')
    for Widget in Optional_Frame.winfo_children():
        Widget.destroy()
    
        
            

reset_btn = Button(window, text = 'Reset Entries', command = reset, bg = 'black').place( x= 490, y = 550)



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