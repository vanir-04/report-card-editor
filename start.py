from tkinter import *
from tkinter import font
import bcrypt
import main_backend
print('function name is', __name__)
import packages.functions
import os
import sys
import subprocess
import pkg_resources


required_modules = {'bcrypt', 'datetime', 'reportlab'}
installed_modules = {pkg.key for pkg in pkg_resources.working_set}
missing_modules = required_modules - installed_modules

if missing_modules:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing_modules], stdout=subprocess.DEVNULL)
    print("Required Modules have now been downloaded")
else:
    print("Required Modules exists.")

cur = packages.functions.db.cursor(buffered=True)
packages.functions.master_lists()
cwd = os.path.dirname(os.path.abspath(__file__))

if len(packages.functions.passlist) == 0:
    def showpass(): 
        current_char = pwd.cget('show')
        if current_char == '*':
            pwd.config(show='')
            showbtn.config(image=eyeclosedimg)
        elif current_char == '':
            pwd.config(show='*')
            showbtn.config(image=eyeimg)
        else:
            pass

    def admreg():
        if pwdvar.get() == '' or pwdvar.get() != repwdvar.get():
            start_try_lbl = Label(start, text="Passwords do not match.", fg="#fb3934", font=('Tw Cen MT', 11))
            start_try_lbl.place(relx=0.5, rely=0.85, anchor='center')
        elif pwdvar.get() == repwdvar.get():
            passhash = bcrypt.hashpw((pwdvar.get()).encode(), bcrypt.gensalt())
            q = '''INSERT INTO admin (Password) VALUES (%s)'''
            cur.execute(q, (passhash,))
            packages.functions.db.commit()
            packages.functions.master_lists()
            start.destroy()
            import editor_gui
        else:
            pass
    start = Tk()

    defaultFont = font.nametofont("TkDefaultFont")
    defaultFont.configure(family="Tw Cen MT", size=13)
    start.title('Setup')
    start.iconbitmap(os.path.join(cwd,'assets/setup.ico'))
    start.geometry("410x300")
    start.tk_setPalette(background="#282828", foreground="#ebdbb2")
    start.resizable(0, 0)
    bg = "#282828"
    fg = "#ebdbb2"
    graybox = "#a89984"
    eyeimg = PhotoImage(file="assets/eyescaled.png")
    eyeclosedimg = PhotoImage(file="assets/eye-closed.png")

    title = Label(start, text="Welcome", fg = "#b8bb26", font = ("Bahnschrift",30))
    title.place(relx=0.5,rely=0.075, anchor=CENTER)

    text1 = Label(start, text="A password is required to initialize the program.\nThis password will also be used for admin mode.\n\nEnter a password:", fg=fg, justify="left")
    text1.place(relx=0.5,rely=0.325, anchor="center")

    pwdvar = StringVar()
    pwdvar.set('')
    pwd = Entry(start, textvariable=pwdvar, width=25, justify='center',show='*', selectbackground=fg, selectforeground=bg)
    pwd.place(relx=0.63,rely=0.425, anchor="center")
    showbtn = Button(start, image=eyeimg, command=showpass, borderwidth=0)
    showbtn.place(relx=0.83,rely=0.395)

    text2 = Label(start, text="Re-enter Password:", fg=fg, justify='left')
    text2.place(relx=0.264, rely=0.55, anchor='center')

    repwdvar = StringVar()
    repwdvar.set('')
    repwd = Entry(start, textvariable=repwdvar, width=25, justify='center', show='*', selectbackground=fg, selectforeground=bg)
    repwd.place(relx=0.63,rely=0.55, anchor="center")

    regbutton = Button(start, text='Register', command=admreg)
    regbutton.place(relx=0.5, rely=0.725, anchor='center')

    start.mainloop()

else:
    import editor_gui
