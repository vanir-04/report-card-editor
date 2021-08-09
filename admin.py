from tkinter import *
from tkinter import ttk
from tkinter import font
import packages.functions
import os

packages.functions.login()
cur = packages.functions.db.cursor()

# Functions #

def sch_add():
    def close():
        popup.destroy()

    school = schoolvar.get()
    
    try:
        cur.execute("USE report_card_db;")
    
        cur.execute('INSERT INTO schools (Name) \
            VALUES ("'+school+'");')
        packages.functions.db.commit()
    except:
        popup = Tk()
        popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
        popup.geometry("255x150+572+340")
        popup.title("Error!")
        popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

        error = Label(popup, text="School already exists", font=("Bahnschrift", 17), fg="#fb4934")
        error.place(x=8,y=25)

        okbutton = Button(popup, text="Ok", command=close, width=10)
        okbutton.place(x=85,y=90)
    
    schooltree.delete(*schooltree.get_children())
    packages.functions.master_lists()
    for i in packages.functions.schoollist:
        schooltree.insert('','end',values=(i))

def sch_delete():
    def close():
        popupwarn.destroy()
    
    def confirm():
        school = schoolvar.get()
        try:
            cur.execute('DELETE FROM student WHERE SchoolName = "'+str(school)+'";')
            cur.execute('DELETE FROM schools WHERE Name = "'+str(school)+'";')
            packages.functions.db.commit()
            schooltree.delete(*schooltree.get_children())
            cur.execute("SELECT Name FROM schools")
            row = cur.fetchall()
            for rw in row:
                schooltree.insert('','end',iid=None,text="test",values=(rw[0]))
                
        except:
            pass
        popupwarn.destroy()

    popupwarn = Tk()  

    popupwarn.iconbitmap(os.path.join(cwd,"assets/confirm.ico"))
    popupwarn.geometry("255x150+572+340")
    popupwarn.title("Confirmation")
    popupwarn.tk_setPalette(background="#282828", foreground="#ebdbb2")

    warninglbl = Label(popupwarn, text="Are you sure?\nThis will delete ALL\ndata for the school", font=("Bahnschrift", 14), fg="#fb4934")
    warninglbl.place(relx=0.5,rely=0.3, anchor=CENTER)

    okbutton = Button(popupwarn, text="Confirm", command=confirm, width=10)
    okbutton.place(relx=0.7,rely=0.7, anchor=CENTER)

    cnclbutton = Button(popupwarn, text="Cancel", command=close,width=10)
    cnclbutton.place(relx=0.3,rely=0.7, anchor=CENTER)
    popupwarn.mainloop()


def class_add():
    pass

def class_delete():
    pass

def section_add():
    pass

def section_delete():
    pass

def sub_add():
    pass

def sub_delete():
    pass

# Initialization #

admin = Tk()

packages.functions.master_lists()
cwd = os.path.dirname(os.path.abspath(__file__))

canvas1 = Canvas()
canvas1.config(width='920', height='450')
line1 = canvas1.create_line(230,50,230,768, fill='#458588', width=2)
line2 = canvas1.create_line(462,50,462,768, fill='#458588', width=2)
line3 = canvas1.create_line(694,50,694,768, fill='#458588', width=2)
line4 = canvas1.create_line(0,50,1366,50, fill='#fb4934', width=3)
canvas1.pack()

defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Tw Cen MT", size=13)
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Tw Cen MT", size=13)
admin.title('Admin')
admin.iconbitmap(os.path.join(cwd,'assets/admin.ico'))
admin.geometry("920x450")
admin.tk_setPalette(background="#282828", foreground="#ebdbb2")
admin.resizable(0, 0)
bg = "#282828"
fg = "#ebdbb2"
graybox = "#a89984"

title = Label(admin, text="Admin Mode", fg = "#b8bb26", font = ("Bahnschrift",30))
title.place(relx=0.5, rely=0.1, anchor=CENTER)

# Schools #

schools = Label(admin, text="Schools", fg=fg, font=("Bahnschrift",23))
schools.place(relx=0.125, rely=0.2, anchor=CENTER)

schoolvar = StringVar()
schooltxt = Entry(admin, textvariable=schoolvar, selectbackground=fg, selectforeground=bg, justify='center', width=30)
schooltxt.place(relx=0.123, rely=0.3, anchor=CENTER)

addschool = Button(admin, text="Add", command=sch_add, width=7, fg="#b8bb26")
addschool.place(relx=0.075, rely=0.393, anchor=CENTER)

delschool = Button(admin, text="Delete", command=sch_delete, width=7, fg="#fb4934")
delschool.place(relx=0.175, rely=0.393, anchor=CENTER)

schooltree = ttk.Treeview(admin, columns=('0'), show='headings', height=10)
schooltree.place(relx=0.123, rely=0.72, anchor=CENTER)

schooltree.column('0', width=200, anchor=CENTER)
schooltree.heading('0', text="School Name")

for i in packages.functions.schoollist:
    schooltree.insert('','end',values=(i))

# Classes #

classes = Label(admin, text="Classes", fg=fg, font=("Bahnschrift",23))
classes.place(relx=0.378, rely=0.2, anchor=CENTER)

classvar = StringVar()
classtxt = Entry(admin, textvariable=classvar, selectbackground=fg, selectforeground=bg, justify='center', width=30)
classtxt.place(relx=0.376, rely=0.3, anchor=CENTER)

addclass = Button(admin, text="Add", command=class_add, width=7, fg="#b8bb26")
addclass.place(relx=0.328, rely=0.393, anchor=CENTER)

delclass = Button(admin, text="Delete", command=class_delete, width=7, fg="#fb4934")
delclass.place(relx=0.428, rely=0.393, anchor=CENTER)

classtree = ttk.Treeview(admin, columns=('0'), show='headings', height=10)
classtree.place(relx=0.376, rely=0.72, anchor=CENTER)

classtree.column('0', width=200, anchor=CENTER)
classtree.heading('0', text="Class")

for i in packages.functions.classlist:
    classtree.insert('','end',values=(i))

# Sections #

sections = Label(admin, text="Sections", fg=fg, font=("Bahnschrift",23))
sections.place(relx=0.631, rely=0.2, anchor=CENTER)

sectvar = StringVar()
sectiontxt = Entry(admin, textvariable=sectvar, selectbackground=fg, selectforeground=bg, justify='center', width=30)
sectiontxt.place(relx=0.629, rely=0.3, anchor=CENTER)

addsection = Button(admin, text="Add", command=section_add, width=7, fg="#b8bb26")
addsection.place(relx=0.581, rely=0.393, anchor=CENTER)

delsection = Button(admin, text="Delete", command=section_delete, width=7, fg="#fb4934")
delsection.place(relx=0.681, rely=0.393, anchor=CENTER)

sectiontree = ttk.Treeview(admin, columns=('0'), show='headings', height=10)
sectiontree.place(relx=0.629, rely=0.72, anchor=CENTER)

sectiontree.column('0', width=200, anchor=CENTER)
sectiontree.heading('0', text="Section")

for i in packages.functions.sectionlist:
    sectiontree.insert('','end',values=(i))

# Subjects #

subjects = Label(admin, text="Subjects", fg=fg, font=("Bahnschrift",23))
subjects.place(relx=0.880, rely=0.2, anchor=CENTER)

subvar = StringVar()
subtxt = Entry(admin, textvariable=subvar, selectbackground=fg, selectforeground=bg, justify='center', width=30)
subtxt.place(relx=0.878, rely=0.3, anchor=CENTER)

addsub = Button(admin, text="Add", command=sub_add, width=7, fg="#b8bb26")
addsub.place(relx=0.830, rely=0.393, anchor=CENTER)

delsub = Button(admin, text="Delete", command=sub_delete, width=7, fg="#fb4934")
delsub.place(relx=0.930, rely=0.393, anchor=CENTER)

subtree = ttk.Treeview(admin, columns=('0'), show='headings', height=10)
subtree.place(relx=0.878, rely=0.72, anchor=CENTER)

subtree.column('0', width=200, anchor=CENTER)
subtree.heading('0', text="Subject")

for i in packages.functions.sublist:
    subtree.insert('','end',values=(i))

admin.mainloop()