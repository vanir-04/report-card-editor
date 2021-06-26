from tkinter import *
import re
from tkinter import font
import packages.functions
import main_backend
import tkPDFViewer

### FUNCTIONS ###

def studentsubmit():
    stud_err = StringVar()
    name = (FirstNam_txt.get() + ' ' + LastNam_txt.get())
    admno = str(Adm_txt.get())
    gender = gendervar.get()
    
    global admerror
    admerror = Label(window, textvariable=stud_err, fg="#fb3934")
    admerror.place(x=20,y=325)

    admlist = []
    cur = packages.functions.db.cursor(buffered=True)
    cur.execute("SELECT AdmissionNo FROM student;")

    for i in cur:
        admlist.append(i)

    if any(admno in s for s in admlist):
        adm_exist = True
    else:
        adm_exist = False

    if adm_exist == True:
        stud_err.set("Please enter a unique Admission No.")

    else:
        cur = packages.functions.db.cursor(buffered=True)
        cur.execute("USE report_card_db;")
    
        cur.execute('INSERT INTO student (AdmissionNo, Name, Gender) VALUES ("'+admno+'", "'+name+'", "'+gender+'");')
        packages.functions.db.commit()
        print("Commit into student successful.")

def semestersubmit():
    admno = str(Adm_txt.get())
    classname_raw = classvar.get()
    section_raw = sectionvar.get()
    rollno = Roll_txt.get()
    year = year_txt.get()
    
    classname = classname_raw.strip("()',")
    section = section_raw.strip("()',")

    cur = packages.functions.db.cursor(buffered=True)
    
    cur.execute('SELECT StudentID FROM student WHERE AdmissionNo = "'+admno+'";')
    studentid_raw = ''
    for i in cur:
        studentid_raw = str(i)
    studentid = studentid_raw.strip('(),')
    
    cur.execute('SELECT ClassID FROM class WHERE Name = "'+ classname +'";')
    classid_raw = ''
    for i in cur:
        classid_raw = str(i)
    classid = classid_raw.strip('(),')

    cur.execute('SELECT SectionID FROM sections WHERE Name = "' + section + '";')
    sectionid_raw = ''
    for i in cur:
        sectionid_raw = str(i)
    sectionid = sectionid_raw.strip('(),')

    try:
        cur.execute('INSERT INTO academics (StudentID, Year, ClassID, SectionID, RollNo) VALUES ('+studentid+', '+year+', '+classid+', '+sectionid+', '+rollno+');')
        packages.functions.db.commit()
        print("Commit into academics successful.")
    except:
        aca_error = Label(window, text="Record already exists.", fg='#fb3934')
        aca_error.place(x=65,y=700)
    finally:
        cur.execute('ALTER TABLE academics AUTO_INCREMENT=1')

def marksubmit():
    subject = subvar.get()
    marks = marks_obt.get()
    totalmarks = total_mks.get()
    date = date_inp.get()
    exam = exam_text.get()

    print(subject)
    print(marks)
    print(totalmarks)
    print(date)
    print(exam)

def reset():
    admerror.destroy()

packages.functions.master_lists()

### WINDOW ###

window=Tk()

# Canvas
canvas1 = Canvas()
canvas1.config(width='1366', height='768')
line1 = canvas1.create_line(290,60,290,768,fill='#458588',width=2, dash = (2,5))
line2 = canvas1.create_line(0,60,1366,60, fill = '#fb4934', width = 3)
canvas1.pack()

# Set Window Configurations
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Tw Cen MT", size=13)
window.title('Editor')
window.geometry("1366x768")
window.tk_setPalette(background="#282828", foreground="#ebdbb2")
bg = "#282828"
fg = "#ebdbb2"
graybox = "#a89984"

### WIDGETS ###

# Title
Topic = Label(window, text="Student Marksheet", fg = "#b8bb26", font = ("Bahnschrift",30))
Topic.place(x=500,y=29)

# Headers
acad_lbl = Label(window, text="Academic Data", font=("Bahnschrift",20))
acad_lbl.place(x=480, y=125)

Data_lbl = Label(window, text="Student Data", font = ("Bahnschrift",20))
Data_lbl.place(x = 60, y = 125) 

sem_lbl = Label(window, text="Semester Data", font=('Bahnschrift', 20))
sem_lbl.place(x=50, y=480)

## STUDENT INFO ##

# Student Details
FirstNam_lbl = Label(window, text = "First Name")
FirstNam_lbl.place(x = 30, y = 200)
FirstNam_txt = Entry(window, bd = 2, selectbackground=fg, selectforeground=bg)
FirstNam_txt.place(x = 130, y = 202)

LastNam_lbl = Label(window, text = "Last Name")
LastNam_lbl.place(x=30 , y=250 )
LastNam_txt = Entry(window, bd = 2, selectbackground=fg, selectforeground=bg)
LastNam_txt.place(x = 130, y = 252 )

Adm_lbl = Label(window, text = "Admission No.")
Adm_lbl.place(x = 30, y = 300)
Adm_txt = Entry(window, bd = 2, selectbackground=fg, selectforeground=bg)
Adm_txt.place(x = 130, y = 302)

# Gender-selection (yes there are only 2 genders boohooo)
gendervar = StringVar()
gendervar.set(' ')

Gender_lbl = Label(window, text = "Gender")
Gender_lbl.place(x = 30, y = 350)
Male = Radiobutton(window, text ="Male",variable = gendervar, value = "Male", selectcolor = bg)
Male.place(x = 110, y = 349)

Female = Radiobutton(window, text = "Female",variable = gendervar, value = "Female", selectcolor = bg)
Female.place(x = 190, y = 349)

## Semester Data
standard = Label(window, text = "Class")
standard.place(x = 30, y = 560)
section = Label(window, text = "Section")
section.place(x = 130, y = 560)

classvar= StringVar()
classvar.set("")

sectionvar = StringVar()
sectionvar.set("")

classdrop = OptionMenu(window, classvar, *packages.functions.classlist)
classdrop.place(x = 70, y = 558)

sectiondrop = OptionMenu(window, sectionvar, *packages.functions.sectionlist)
sectiondrop.place(x = 185, y= 558)

Roll_lbl = Label(window, text = "Roll No.")
Roll_lbl.place(x = 30, y = 610)
Roll_txt = Entry(window, bd =2, width=4, selectbackground=fg, selectforeground=bg)
Roll_txt.place(x = 90, y = 612)

year_lbl = Label(window, text = "Year")
year_lbl.place(x = 130, y = 610)
year_txt = Entry(window, bd =2, width=4, selectbackground=fg, selectforeground=bg)
year_txt.place(x=170,y=612)

# Submit button
student_btn = Button(window, text = "Add Student to Database", command = studentsubmit)
student_btn.place(x=50,y = 400)

semester_btn = Button(window, text = "Add Semester to Database", command = semestersubmit)
semester_btn.place(x=45,y = 660)

## ADDING/EDITING EXAM RESULTS ##

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

marksvar = StringVar()
marks_obt = Entry(window, textvariable=marksvar, width=3)
marks_obt.place(x=390,y=254)

slash_lbl = Label(window, text='/', font=('Bahnschrift', 23))
slash_lbl.place(x=420,y=240)

totalvar = StringVar()
total_mks = Entry(window, textvariable=totalvar, width=3)
total_mks.place(x=445,y=254)

date_lbl = Label(window, text="Date")
date_lbl.place(x=575, y=250)

datevar = StringVar()
datevar.set("YYYY-MM-DD")
date_inp = Entry(window, textvariable=datevar)
date_inp.place(x=675,y=253 )

reset_btn = Button(window, text = "Reset", command = reset)
reset_btn.place(x=450,y = 440)

window.mainloop()