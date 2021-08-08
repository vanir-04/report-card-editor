from tkinter import *
from tkinter import font
from tkinter.filedialog import asksaveasfile
from mysql.connector.errors import IntegrityError, ProgrammingError
import packages.functions
import os
import main_backend
from tkinter import ttk
from datetime import date
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table
from reportlab.pdfgen import canvas

cwd = os.path.dirname(os.path.abspath(__file__))

### FUNCTIONS ###

def studentsubmit():
    def close():
        popup.destroy()

    name = (firstnamevar.get() + ' ' + lastnamevar.get())
    admno = str(admvar.get())
    gender = gendervar.get()
    school = schoolname.get()
    try:
        cur = packages.functions.db.cursor(buffered=True)
        cur.execute("USE report_card_db;")
    
        cur.execute('INSERT INTO student (AdmissionNo, Name, Gender, SchoolName) \
            VALUES ("'+admno+'", "'+name+'", "'+gender+'", "'+school+'");')
        packages.functions.db.commit()
    except:
        popup = Tk()
        popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
        popup.geometry("255x150+572+340")
        popup.title("Error!")
        popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

        error = Label(popup, text="Student already exists", font=("Bahnschrift", 17), fg="#fb4934")
        error.place(x=8,y=25)

        okbutton = Button(popup, text="Ok", command=close, width=10)
        okbutton.place(x=85,y=90)
    
    stutree.delete(*stutree.get_children())
    cur.execute("SELECT AdmissionNo, Name, Gender FROM student")
    row = cur.fetchall()
    for rw in row:
        stutree.insert('','end',iid=None,text="test",values=(rw[0],rw[1],rw[2])) 

def acasubmit():
    def close():
        popup.destroy()

    admno = str(admvar.get())
    classname_raw = classvar.get()
    section_raw = sectionvar.get()
    rollno = rollvar.get()
    year = yearvar.get()
    subject_raw = str(subvar.get())
    marks = marksvar.get()
    totalmarks = totalvar.get()
    exam = examvar.get()

    classname = classname_raw.strip("()',")
    section = section_raw.strip("()',")
    subject = subject_raw.strip("'(),")

    cur = packages.functions.db.cursor(buffered=True)

    cur.execute('SELECT SubjectID FROM subjects WHERE Name = "' + subject + '";')
    subjectid_raw = ''
    for i in cur:
        subjectid_raw = str(i)
    subjectid = subjectid_raw.strip('(),')

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

    sem_fail_integ = False
    sem_fail_prog = False
    mark_fail_integ = False
    mark_fail_prog = False

    if int(marks) > int(totalmarks):
        popup = Tk()
        popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
        popup.geometry("255x150+572+340")
        popup.title("Error!")
        popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

        error = Label(popup, text="Marks cannot be more\nthan the total.", font=("Bahnschrift", 17), fg="#fb4934")
        error.place(relx=0.5,y=40, anchor=CENTER)

        okbutton = Button(popup, text="Ok", command=close, width=10)
        okbutton.place(x=85,y=90)
    elif int(marks) < 0:
        popup = Tk()
        popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
        popup.geometry("255x150+572+340")
        popup.title("Error!")
        popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

        error = Label(popup, text="Marks cannot be\nnegative.", font=("Bahnschrift", 17), fg="#fb4934")
        error.place(relx=0.5,y=40, anchor=CENTER)

        okbutton = Button(popup, text="Ok", command=close, width=10)
        okbutton.place(x=85,y=90)
    else:
        try:
            cur.execute('INSERT INTO academics (StudentID, Year, ClassID, SectionID, RollNo, SubjectID) \
                VALUES ('+studentid+', '+year+', '+classid+', '+sectionid+', '+rollno+', '+subjectid+');')
            packages.functions.db.commit()
            sem_fail_integ = False
            sem_fail_prog = False
        except IntegrityError:
            sem_fail_integ = True
        except ProgrammingError:
            sem_fail_prog = True

        cur.execute('SELECT AcademicID FROM academics WHERE \
        StudentID='+studentid+' \
        AND ClassID='+classid+' \
        AND Year='+year+' \
        AND SubjectID='+subjectid+';')

        academicid_raw = ''
        
        for i in cur:
            academicid_raw = str(i)
        
        academicid = academicid_raw.strip("'(),")

        try:
            cur.execute('INSERT INTO exam (AcademicID, Name, TotalMarks, MarksObtained, Year) \
                VALUES ('+academicid+', "'+exam+'", '+totalmarks+', '+marks+', '+year+');')
            packages.functions.db.commit()
            mark_fail_integ = False
            mark_fail_prog = False
        except IntegrityError:
            mark_fail_integ = True
        except ProgrammingError:
            mark_fail_prog = True

        if sem_fail_prog == False and mark_fail_prog == False and sem_fail_integ == False and mark_fail_integ == False:
            pass

        elif sem_fail_integ == True and mark_fail_integ == True:
            popup = Tk()
            popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
            popup.geometry("255x150+572+340")
            popup.title("Error!")
            popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

            error = Label(popup, text="Record already exists", font=("Bahnschrift", 17), fg="#fb4934")
            error.place(x=8,y=25)

            okbutton = Button(popup, text="Ok", command=close, width=10)
            okbutton.place(x=85,y=90)
        elif sem_fail_integ == True and mark_fail_integ == False:
            pass
        elif sem_fail_prog == True and mark_fail_prog == True:
            popup = Tk()
            popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
            popup.geometry("255x150+572+340")
            popup.title("Error!")
            popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

            error = Label(popup, text="Student not found,\nplease add student", font=("Bahnschrift", 17), fg="#fb4934")
            error.place(x=27,y=20)

            okbutton = Button(popup, text="Ok", command=close, width=10)
            okbutton.place(x=85,y=90)
        else:
            pass
        
        markstree.delete(*markstree.get_children())
        
        sItem = stutree.focus()
        svalues = stutree.item(sItem)
        
        cur.execute('SELECT a.Year, \
            c.Name, \
            se.Name, \
            a.RollNo, \
            e.Name, \
            su.Name, \
            e.MarksObtained, \
            e.TotalMarks \
            FROM academics a \
                INNER JOIN class c \
                    ON c.ClassID = a.ClassID \
                INNER JOIN sections se \
                    ON se.SectionID = a.SectionID \
                INNER JOIN student st \
                    ON st.StudentID = a.StudentID \
                INNER JOIN subjects su \
                    ON su.SubjectID = a.SubjectID \
                INNER JOIN exam e \
                    ON e.AcademicID = a.AcademicID \
            WHERE st.AdmissionNo = "'+str(svalues['values'][0])+'"\
            ORDER BY a.Year, c.Name, se.Name, a.RollNo, e.Name, su.Name;')
        
        arow = cur.fetchall()

        for arw in arow:
            markstree.insert('','end',values=(arw[0],arw[1],arw[2],arw[3],arw[4],arw[5],arw[6],arw[7]))

def s_fetch(event):
    sItem = stutree.focus()
    svalues = stutree.item(sItem)
    stuname = (svalues['values'][1]).split()
    firstnamevar.set(stuname[0])
    lastnamevar.set(stuname[1])
    admvar.set(svalues['values'][0])
    gendervar.set(svalues['values'][2])

    cur.execute('SELECT a.Year, \
        c.Name, \
        se.Name, \
        a.RollNo, \
        e.Name, \
        su.Name, \
        e.MarksObtained, \
        e.TotalMarks \
        FROM academics a \
            INNER JOIN class c \
                ON c.ClassID = a.ClassID \
            INNER JOIN sections se \
                ON se.SectionID = a.SectionID \
            INNER JOIN student st \
                ON st.StudentID = a.StudentID \
            INNER JOIN subjects su \
                ON su.SubjectID = a.SubjectID \
            INNER JOIN exam e \
                ON e.AcademicID = a.AcademicID \
        WHERE st.AdmissionNo = "'+str(svalues['values'][0])+'"\
        ORDER BY a.Year, c.Name, se.Name, a.RollNo, e.Name, su.Name;')

    arow = cur.fetchall()

    markstree.delete(*markstree.get_children())

    for arw in arow:
        markstree.insert('','end',values=(arw[0],arw[1],arw[2],arw[3],arw[4],arw[5],arw[6],arw[7]))

def a_fetch(event):
    aItem = markstree.focus()
    avalues = markstree.item(aItem)
    yearvar.set(avalues['values'][0])
    classvar.set(avalues['values'][1])
    sectionvar.set(avalues['values'][2])
    rollvar.set(avalues['values'][3])
    examvar.set(avalues['values'][4])
    subvar.set(avalues['values'][5])
    marksvar.set(avalues['values'][6])
    totalvar.set(avalues['values'][7])

def s_delete():
    def close():
        popupwarn.destroy()
    
    def confirm():
        admno = admvar.get()
        cur.execute('SELECT StudentID FROM student WHERE AdmissionNo = "'+str(admno)+'";')
        admlist = cur.fetchone()
        try:
            cur.execute('DELETE FROM student WHERE AdmissionNo = "'+str(admno)+'";')
            cur.execute('DELETE FROM academics WHERE StudentID = "'+str(admlist[0])+'";')
            packages.functions.db.commit()
            stutree.delete(*stutree.get_children())
            cur.execute("SELECT AdmissionNo, Name, Gender FROM student")
            row = cur.fetchall()
            for rw in row:
                stutree.insert('','end',iid=None,text="test",values=(rw[0],rw[1],rw[2]))
            
            markstree.delete(*markstree.get_children())
        
            sItem = stutree.focus()
            svalues = stutree.item(sItem)
            
            cur.execute('SELECT a.Year, \
                c.Name, \
                se.Name, \
                a.RollNo, \
                e.Name, \
                su.Name, \
                e.MarksObtained, \
                e.TotalMarks \
                FROM academics a \
                    INNER JOIN class c \
                        ON c.ClassID = a.ClassID \
                    INNER JOIN sections se \
                        ON se.SectionID = a.SectionID \
                    INNER JOIN student st \
                        ON st.StudentID = a.StudentID \
                    INNER JOIN subjects su \
                        ON su.SubjectID = a.SubjectID \
                    INNER JOIN exam e \
                        ON e.AcademicID = a.AcademicID \
                WHERE st.AdmissionNo = "'+str(svalues['values'][0])+'"\
                ORDER BY a.Year, c.Name, se.Name, a.RollNo, e.Name, su.Name;')
            
            arow = cur.fetchall()

            for arw in arow:
                markstree.insert('','end',values=(arw[0],arw[1],arw[2],arw[3],arw[4],arw[5],arw[6],arw[7]))
                
        except:
            pass
        popupwarn.destroy()

    popupwarn = Tk()  

    popupwarn.iconbitmap(os.path.join(cwd,"assets/confirm.ico"))
    popupwarn.geometry("255x150+572+340")
    popupwarn.title("Confirmation")
    popupwarn.tk_setPalette(background="#282828", foreground="#ebdbb2")

    warninglbl = Label(popupwarn, text="Are you sure?\nThis will delete ALL\ndata for the student", font=("Bahnschrift", 14), fg="#fb4934")
    warninglbl.place(relx=0.5,rely=0.3, anchor=CENTER)

    okbutton = Button(popupwarn, text="Confirm", command=confirm, width=10)
    okbutton.place(relx=0.7,rely=0.7, anchor=CENTER)

    cnclbutton = Button(popupwarn, text="Cancel", command=close,width=10)
    cnclbutton.place(relx=0.3,rely=0.7, anchor=CENTER)
    popupwarn.mainloop()

def a_delete():
    admno = admvar.get()
    cur.execute('SELECT StudentID FROM student WHERE AdmissionNo = "'+str(admno)+'";')
    admlist = cur.fetchone()
    classname = classvar.get()
    cur.execute('SELECT ClassID FROM class WHERE Name = "'+str(classname)+'";')
    classlist = cur.fetchone()
    subname = subvar.get()
    cur.execute('SELECT SubjectID FROM subjects WHERE Name = "'+str(subname)+'";')
    sublist = cur.fetchone()
    year = yearvar.get()
    cur.execute('SELECT AcademicID from academics WHERE StudentID = "'+str(admlist[0])+'" AND ClassID = "'+str(classlist[0])+'" AND Year = "'+str(year)+'" AND SubjectID = "'+str(sublist[0])+'";')
    a_idlist = cur.fetchone()
    examname = examvar.get()
    cur.execute('DELETE FROM exam WHERE AcademicID = "'+str(a_idlist[0])+'" AND Name = "'+str(examname)+'";')
    packages.functions.db.commit()
    
    markstree.delete(*markstree.get_children())

    sItem = stutree.focus()
    svalues = stutree.item(sItem)
    
    cur.execute('SELECT a.Year, \
        c.Name, \
        se.Name, \
        a.RollNo, \
        e.Name, \
        su.Name, \
        e.MarksObtained, \
        e.TotalMarks \
        FROM academics a \
            INNER JOIN class c \
                ON c.ClassID = a.ClassID \
            INNER JOIN sections se \
                ON se.SectionID = a.SectionID \
            INNER JOIN student st \
                ON st.StudentID = a.StudentID \
            INNER JOIN subjects su \
                ON su.SubjectID = a.SubjectID \
            INNER JOIN exam e \
                ON e.AcademicID = a.AcademicID \
        WHERE st.AdmissionNo = "'+str(svalues['values'][0])+'"\
        ORDER BY a.Year, c.Name, se.Name, a.RollNo, e.Name, su.Name;')
    
    arow = cur.fetchall()

    for arw in arow:
        markstree.insert('','end',values=(arw[0],arw[1],arw[2],arw[3],arw[4],arw[5],arw[6],arw[7]))

def s_update():
    sItem = stutree.focus()
    svalues = stutree.item(sItem)
    name = (firstnamevar.get() + ' ' + lastnamevar.get())
    gender = gendervar.get()
    try:
        padmno = svalues['values'][0]
    except:
        def ok():
            popup.destroy()
        popup = Tk()
        popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
        popup.tk_setPalette(background="#282828", foreground="#ebdbb2")
        popup.title("Error")
        popup.geometry('300x150+550+250')
        errtext = Label(popup, text="Please select student\nto update from list.", font=("Bahnschrift", 19), fg="#fb3934")
        errtext.pack()
        okbutton = Button(popup, text="Ok", command=ok, width=20)
        okbutton.pack(pady=20)
        popup.mainloop()

    nadmno = admvar.get()

    cur = packages.functions.db.cursor(buffered=True)
    cur.execute("USE report_card_db;")

    cur.execute("SELECT StudentID FROM student WHERE AdmissionNo = '"+str(padmno)+"' ;")
    StudID = str(cur.fetchone()).strip("(),")

    try:    
        cur.execute("UPDATE student SET Name = '"+name+"', Gender = '"+gender+"', AdmissionNo = '"+str(nadmno)+"' \
            WHERE StudentID = '"+StudID+"';")
        packages.functions.db.commit()
    except IntegrityError:
        def ok():
            popup.destroy()
        popup = Tk()
        popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
        popup.tk_setPalette(background="#282828", foreground="#ebdbb2")
        popup.title("Error")
        popup.geometry('300x150+550+250')
        errtext = Label(popup, text="Admission Number\nalready exists!", font=("Bahnschrift", 19), fg="#fb3934")
        errtext.pack()
        okbutton = Button(popup, text="Ok", command=ok, width=20)
        okbutton.pack(pady=20)
        popup.mainloop()

    stutree.delete(*stutree.get_children())
    cur.execute("SELECT AdmissionNo, Name, Gender FROM student")
    row = cur.fetchall()
    for rw in row:
        stutree.insert('','end',iid=None,text="test",values=(rw[0],rw[1],rw[2]))

def pdf_gen():
    ########################Fetching Table Data########################
    sItem = stutree.focus()
    svalues = stutree.item(sItem)
    admno = svalues['values'][0]
    Student_ID = []
    cur.execute("select studentID from student where AdmissionNo = '" +str(admno)+ "'; ")
    Student_ = cur.fetchall()
    for [i] in Student_:
        Student_ID.append(i)
    print(Student_ID[0])
    
    #####SUBJECTS#####
    Subject_ID_Statement = ('SELECT SubjectID FROM Academics WHERE StudentID = ')
    Subject_ID_Query = Subject_ID_Statement + str(Student_ID[0])
    cur.execute(Subject_ID_Query)
    Subject_Data = cur.fetchall()
    SubjectID = []
    Subs = []
    Subs1 = []
    Subjects = []
    Select_Statement = "SELECT Name FROM Subjects WHERE SubjectID = "
    
    #Getting Subject ID
    for [x] in Subject_Data:
        SubjectID.append(x)
    print(SubjectID)
    
    #Getting Subjects
    for i in SubjectID:
        Select_Statement_Query = Select_Statement + str(i)
        cur.execute(Select_Statement_Query)
        Data = cur.fetchall()
        Subs.append(Data)
    for [i] in Subs:
        Subs1.append(i)
    for [i] in Subs1:
        Subjects.append(i)
    Subjects.insert(0, 'Subject')
    print(Subjects)
    
    #####NAME, ADMISSION NUMBER, GENDER#####
    General_Details_Statement = ('SELECT AdmissionNo, Name, Gender FROM student WHERE studentID  = ')
    General_Details_Query = General_Details_Statement + str(Student_ID[0])
    cur.execute(General_Details_Query)
    List = cur.fetchall()
    Student_Data = []
    for i in List[0]:
        Student_Data.append(i)
    print(Student_Data)
    
    #####Class, Section, Roll No.#####
    Class_Statement = ('SELECT DISTINCT ClassID, SectionID, RollNo FROM Academics WHERE StudentID = ')
    Class_Query = Class_Statement + str(Student_ID[0])
    cur.execute(Class_Query)
    List1 = cur.fetchall()
    Classroom_Data = []
    print(List1)
    for i in List1[0]:  
        Classroom_Data.append(i)
    print(Classroom_Data)
    
    ###CLASS###
    
    Statement_Class = ('SELECT Name FROM Class WHERE CLassID = ')
    Class_Query = Statement_Class + str(Classroom_Data[0])
    cur.execute(Class_Query)
    Class = cur.fetchall()
    Class_List = []
    for [i] in Class:
        Class_List.append(i)
    print(Class_List)
    
    ###SECTION###
    Statement_Section = ('SELECT Name FROM Sections WHERE SectionID = ')
    Section_Query = Statement_Section + str(Classroom_Data[1])
    cur.execute(Section_Query)
    Section = cur.fetchall()
    Section_List = []
    for [i] in Section:
        Section_List.append(i)
    print(Section_List)
    
    ###ROLL NO###
    #Classroom_Data[2] is the Roll Number
    
    #####MARKS AND EXAM#####
    AcademicID = []
    Academic_ID_Collection = ('SELECT AcademicID FROM Academics WHERE StudentID = ')
    Academic_ID_Query = Academic_ID_Collection + str(Student_ID[0])
    cur.execute(Academic_ID_Query)
    Academic = cur.fetchall()
    for [i] in Academic:
        AcademicID.append(i)
    print(AcademicID)
    
    Marks_Obtained = []
    Total_Marks = []
    
    for x in AcademicID:
        Statement_12 = ('SELECT MarksObtained FROM exam WHERE AcademicID = ')
        Statement_12_Query = Statement_12 + str(x)
        cur.execute(Statement_12_Query)
        Marks = cur.fetchall()
        for [i] in Marks:
            Marks_Obtained.append(i)
    Marks_Obtained.insert(0, 'Marks Scored')
    print(Marks_Obtained)
    for y in AcademicID:
        Statement_101 = ('SELECT TotalMarks FROM exam WHERE AcademicID = ')    
        Statement_101_Query = Statement_101  + str(y)
        cur.execute(Statement_101_Query)
        Total = cur.fetchall()
        for [i] in Total:
            Total_Marks.append(i)
    Total_Marks.insert(0,'Max. Marks')
    print(Total_Marks)  
    
    table_data = []
    for a in (Subjects, Marks_Obtained, Total_Marks):
        table_data.append(a)
    
    print(table_data)
    #################################################################################################################################################

    #Creating PDF Page
    
    #pdf_name = PDF_Name_Text.get() + '.pdf'
    filetype = [('PDF File', '*.pdf')]
    filename = asksaveasfile(filetypes=filetype, defaultextension=filetype)
    updated_pdf_path = filename.name
    pdf = canvas.Canvas(updated_pdf_path, pagesize = A4 )
    pdf.drawImage((os.path.join(cwd,'assets/LightBlue_Background.png')), 0, 0, 1000, 1000)
    pdf.setTitle(title = 'pdf_gen' )
    pdf.setFont('Helvetica', 17)
    pdf.drawString(x = 26, y = 800, text = str(current_date))
    pdf.setFont('Helvetica-Bold', 20)
    pdf.drawString(x = 160, y = 800, text = School_txt.get())
    pdf.setLineWidth(4)
    pdf.line(0, 780, 700, 780)
    pdf.setFont('Helvetica', 16)
    pdf.drawString(x = 230, y = 750, text = 'Student Report Card')
    pdf.setLineWidth(2)
    pdf.line(230, 749, 376, 749)
    pdf.setLineWidth(4)
    pdf.rect(1, 1, 593, 840, fill = 0)
    pdf.setLineWidth(1)
    pdf.setFont('Helvetica', 14)
    pdf.drawString(60, 700, text = 'Name :')
    pdf.drawString(108, 700, text = Student_Data[1])
    pdf.drawString(60, 660, text = 'Adm No. :')
    pdf.drawString(128, 660, text = Student_Data[0])
    pdf.drawString(400, 700, text = 'Gender :')
    pdf.drawString(460, 700, text = Student_Data[2])
    pdf.drawString(400, 660, text = 'Roll No. :')
    pdf.drawString(462, 660, text = str(Classroom_Data[2]))
    def dotted_lines(pdf):
        pdf.setDash(1, 1) 
        pdf.line(0, 684, 800, 684)
        pdf.line(300, 650, 300, 720)
        pdf.line(0,650,800,650)
        pdf.line(0,720,800,720)
        pdf.line(130, 1000, 130, 780)
    dotted_lines(pdf)
        
    pdf.setDash(10000000,1)
    table = Table(table_data)
    table.setStyle([ \
      ('GRID', (0,0), (0, -1), 2, colors.black),
      ('GRID', (0, 0), (-1, -1), 0.5 ,colors.black), \
      ('TEXTCOLOR', (0,0), (-1, -1), colors.black), \
      ('ALIGN', (0,0,), (-1, -1), 'LEFT'), \
      ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), \
      ('FONTSIZE', (0,0), (-1,-1), 12)])
    
        
    table.wrapOn(pdf, 100, 400)
    table.drawOn(pdf, 20, 470)
    pdf.save()
    print("PDF Report File has been created")
    print(updated_pdf_path)

packages.functions.master_lists()

### WINDOW ###

window=Tk()

# Canvas
canvas1 = Canvas()
canvas1.config(width='1280', height='720')
line1 = canvas1.create_line(360,60,360,768, fill='#458588', width=2)
line2 = canvas1.create_line(910,60,910,768, fill='#458588', width=2)
line3 = canvas1.create_line(0,60,1366,60, fill='#fb4934', width=3)
canvas1.pack()

# Set Window Configurations
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Tw Cen MT", size=13)
window.title('Editor')
window.iconbitmap(os.path.join(cwd,'assets/book.ico'))
window.geometry("1280x720+30+0")
window.tk_setPalette(background="#282828", foreground="#ebdbb2")
window.resizable(0, 0)
bg = "#282828"
fg = "#ebdbb2"
graybox = "#a89984"

### WIDGETS ###

# Assigning Date Variable
current_date = date.today()

# Title
title = Label(window, text="Student Marksheet", fg = "#b8bb26", font = ("Bahnschrift",30))
title.place(relx=0.5,rely=0.075, anchor=CENTER)

# Headers
acad_lbl = Label(window, text="Academic Data", font=("Bahnschrift",20))
acad_lbl.place(relx=0.5, y=118, anchor=CENTER)

stud_lbl = Label(window, text="Student Data", font = ("Bahnschrift",20))
stud_lbl.place(x = 103, y = 100) 

pdf_lbl = Label(window, text="Create PDF", font = ("Bahnschrift",20))
pdf_lbl.place(x = 1027, y = 100) 

## STUDENT INFO ##
# School Name
School_lbl = Label(window, text = "School Name")
School_lbl.place(x = 45, y = 150)
schoolname = StringVar()
School_txt = Entry(window, textvariable=schoolname,selectbackground=fg, selectforeground=bg, justify='center', width=30)
School_txt.place(x = 145, y = 152)

# Student Details
firstname_lbl = Label(window, text = "First Name")
firstname_lbl.place(x = 65, y = 200)
firstnamevar = StringVar()
firstname_txt = Entry(window, textvariable=firstnamevar, selectbackground=fg, selectforeground=bg, justify='center')
firstname_txt.place(x = 165, y = 202)

lastname_lbl = Label(window, text = "Last Name")
lastname_lbl.place(x=65 ,y=250 )
lastnamevar = StringVar()
lastname_txt = Entry(window, textvariable=lastnamevar, selectbackground=fg, selectforeground=bg, justify='center')
lastname_txt.place(x = 165, y = 252 )

adm_lbl = Label(window, text = "Admission No.")
adm_lbl.place(x = 65, y = 300)
admvar = StringVar()
adm_txt = Entry(window, textvariable=admvar, selectbackground=fg, selectforeground=bg, justify='center')
adm_txt.place(x = 165, y = 302)
 
# Gender-selection
gendervar = StringVar()
gendervar.set(' ')

gender_lbl = Label(window, text = "Gender")
gender_lbl.place(x = 65, y = 350)
male = Radiobutton(window, text ="Male",variable = gendervar, value = "Male", selectcolor = bg)
male.place(x = 145, y = 349)

female = Radiobutton(window, text = "Female",variable = gendervar, value = "Female", selectcolor = bg)
female.place(x = 225, y = 349)

# Student section buttons
addstudent_btn = Button(window, text = "Add", command = studentsubmit, width=7, fg="#b8bb26")
addstudent_btn.place(x=140,y = 400)

update_btn = Button(window, text = "Update", command = s_update, width=7, fg="#83a598")
update_btn.place(x = 60, y = 400)

delstudent_btn = Button(window, text = "Delete", command=s_delete, width=7, fg="#fb4934")
delstudent_btn.place(x=220, y = 400)

## ADDING/EDITING EXAM RESULTS ##

class_lbl = Label(window, text = "Class")
class_lbl.place(x = 415, y = 203)

classvar= StringVar()
classvar.set("None")
classdrop = OptionMenu(window, classvar,  *packages.functions.classlist)
classdrop.place(x = 475, y = 200)

roll_lbl = Label(window, text = "Roll No.")
roll_lbl.place(x = 660, y = 200)
rollvar = StringVar()
roll_txt = Entry(window, textvariable=rollvar, selectbackground=fg, selectforeground=bg, justify='center')
roll_txt.place(x = 760, y = 203)

section = Label(window, text = "Section")
section.place(x = 415, y = 253)

sectionvar = StringVar()
sectionvar.set("None")    
sectiondrop = OptionMenu(window,sectionvar,*packages.functions.sectionlist)
sectiondrop.place(x = 475, y= 250)

year_lbl = Label(window, text="Year of Session", font=('Tw Cen MT', 12))
year_lbl.place(x=660, y=250)

yearvar = StringVar()
year_txt = Entry(window, textvariable=yearvar, selectbackground=fg, selectforeground=bg, justify='center')
year_txt.place(x=760,y=253)

sub_lbl = Label(window, text="Subject")
sub_lbl.place(x=415,y=303)

subvar = StringVar()
subvar.set("None")
subject_drop = OptionMenu(window, subvar, *packages.functions.sublist)
subject_drop.place(x=475,y=300)

exam_lbl = Label(window, text="Exam Name")
exam_lbl.place(x=660,y=300)

examvar = StringVar()
exam_text = Entry(window, textvariable=examvar, selectbackground=fg, selectforeground=bg, justify='center')
exam_text.place(x=760,y=303)

marks_lbl = Label(window, text="Marks")
marks_lbl.place(x=415,y=350)

marksvar = StringVar()
marks_obt = Entry(window, textvariable=marksvar, width=3, selectbackground=fg, selectforeground=bg, justify='center')
marks_obt.place(x=475,y=354)

slash_lbl = Label(window, text='/', font=('Bahnschrift', 23))
slash_lbl.place(x=505,y=340)

totalvar = StringVar()
total_mks = Entry(window, textvariable=totalvar, width=3, selectbackground=fg, selectforeground=bg, justify='center')
total_mks.place(x=530,y=354)

stutree = ttk.Treeview(window, columns=('0', '1', '2'), show='headings', height=8)
stutree.place(x=12, y=465)

stutree.column('0', width=100, anchor=CENTER)
stutree.column('1', width=140, anchor=CENTER)
stutree.column('2', width=80, anchor=CENTER)

stutree.heading('0', text="Admission No.")
stutree.heading('1', text="Name")
stutree.heading('2', text="Gender")

stutree.bind("<ButtonRelease-1>", s_fetch)

stuscrollbar = ttk.Scrollbar(window, orient="vertical", command=stutree.yview)
stuscrollbar.place(x=10+321, y=465, height=160+27)

stutree.configure(yscrollcommand=stuscrollbar.set)

cur = packages.functions.db.cursor()
cur.execute("SELECT AdmissionNo, Name, Gender FROM student")
srow = cur.fetchall()
for rw in srow:
    stutree.insert('','end',values=(rw[0],rw[1],rw[2]))

markstree = ttk.Treeview(window, columns=('1', '2', '3', '4', '5', '6', '7', '8'), show='headings', height=11)
markstree.place(x=373, y=405)

markstree.bind("<ButtonRelease-1>", a_fetch)

markscrollbar = ttk.Scrollbar(window, orient="vertical", command=markstree.yview)
markscrollbar.place(x=880, y=405, height=247)

markstree.configure(yscrollcommand=markscrollbar.set)

markstree.column('1', width=50, anchor=CENTER)
markstree.column('2', width=40, anchor=CENTER)
markstree.column('3', width=50, anchor=CENTER)
markstree.column('4', width=50, anchor=CENTER)
markstree.column('5', width=90, anchor=CENTER)
markstree.column('6', width=150, anchor=CENTER)
markstree.column('7', width=40, anchor=CENTER)
markstree.column('8', width=35, anchor=CENTER)

markstree.heading('1', text="Year")
markstree.heading('2', text="Class")
markstree.heading('3', text="Section")
markstree.heading('4', text="Roll No.")
markstree.heading('5', text="Exam")
markstree.heading('6', text="Subject")
markstree.heading('7', text="Marks")
markstree.heading('8', text="Total")

submit_btn = Button(window, text="Add", command=acasubmit, width=7, fg="#b8bb26")
submit_btn.place(x=570, y=345)

acadelete_btn = Button(window, text="Delete", command=a_delete, width=7, fg="#fb4934")
acadelete_btn.place(x=650, y=345)

pdf_gen_btn = Button(window, text = "Create PDF", command = pdf_gen)
pdf_gen_btn.place(x=955, y=200)

#PDF_Name = Label(window, text = 'Name of PDF :')
#PDF_Name.place(x = 950, y  = 150)
#PDF_Variable = StringVar()
#PDF_Name_Text = Entry(window, textvariable=PDF_Variable, selectbackground=fg, selectforeground=bg, justify='center')
#PDF_Name_Text.place(x = 1050, y = 150)

window.mainloop()
