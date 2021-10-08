from tkinter import *
from tkinter import font
import tkinter
from tkinter.filedialog import asksaveasfile
import bcrypt
from mysql.connector.errors import IntegrityError, ProgrammingError
import packages.functions
import os
from tkinter import ttk
from datetime import date
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table
from reportlab.pdfgen import canvas

cur = packages.functions.db.cursor(buffered=True)
print("function name",__name__)
packages.functions.master_lists()
cwd = os.path.dirname(os.path.abspath(__file__))

### FUNCTIONS ###

def studentsubmit():
    def close():
        popup.destroy()

    name = (firstnamevar.get() + ' ' + lastnamevar.get())
    admno = str(admvar.get())
    gender = gendervar.get()
    school = schoolvar.get()
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

    cur.execute('SELECT StudentID FROM student WHERE AdmissionNo = "'+str(svalues['values'][0])+'";')
    s_id = str(cur.fetchone()).strip('(,)')

    cur.execute('SELECT DISTINCT Year FROM academics WHERE StudentID = "'+str(s_id)+'";')
    global yearlist
    yearlist = []
    for i in cur.fetchall():
        yearlist.append(str(i).strip('(,)'))

    yeardrop['menu'].delete(0, 'end')
    for y in yearlist:
        yearcmd = tkinter._setit(yeardropvar, y, examchng)
        yeardrop['menu'].add_command(label=y, command=yearcmd)

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

    Marks_Obtained_Number  = 0
    for j in range(1, len(Marks_Obtained)):
        Marks_Obtained_Number += int(Marks_Obtained[j])

    for y in AcademicID:
        Statement_101 = ('SELECT TotalMarks FROM exam WHERE AcademicID = ')    
        Statement_101_Query = Statement_101  + str(y)
        cur.execute(Statement_101_Query)
        Total = cur.fetchall()
        for [i] in Total:
            Total_Marks.append(i)
    Total_Marks.insert(0,'Max. Marks')
    print(Total_Marks)
    
    Total_Marks_Number = 0
    for w in range(1, len(Total_Marks)):
        Total_Marks_Number += int(Total_Marks[w])
    
    print(Marks_Obtained_Number)
    print(Total_Marks_Number)

    marks_table_data = []
    for a in (Subjects, Marks_Obtained, Total_Marks):
        marks_table_data.append(a)
    
    print(marks_table_data)

    signature_table_data = [["Parent's Signature", "Student's Signature", "Principal's Signature"]]
    #################################################################################################################################################

    
    #Creating PDF Page
    global updated_pdf_path
    #pdf_name = PDF_Name_Text.get() + '.pdf'
    filetype = [('PDF File', '*.pdf')]
    filename = asksaveasfile(filetypes=filetype, defaultextension=filetype)
    updated_pdf_path = filename.name
    name_of_file = updated_pdf_path.split('/')
    pdf = canvas.Canvas(updated_pdf_path, pagesize = A4 )
    pdf.setTitle(title = 'pdf_gen' )
    pdf.setFont('Helvetica', 17)
    pdf.drawString(x = 26, y = 800, text = str(current_date))
    pdf.setFont('Helvetica-Bold', 20)
    pdf.drawString(x = 160, y = 800, text = schoolvar.get())
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
    pdf.drawString(60, 620, text = 'Exam :')
    pdf.drawString(108, 620, text = examdropvar.get())
    pdf.drawString(400, 620, text = 'Session:')
    year_difference = int(yeardropvar.get()) + 1
    session_year = str(yeardropvar.get()) + "-" + str(year_difference)
    pdf.drawString(462, 620, text = session_year)
    def dotted_lines(pdf):
        pdf.setDash(1, 1) 
        pdf.line(0,610, 800, 610)
        pdf.line(0, 684, 800, 684)
        pdf.line(300, 610, 300, 720)
        pdf.line(0,650,800,650)
        pdf.line(0,720,800,720)
        pdf.line(130, 1000, 130, 780)
    dotted_lines(pdf)
    
    scored_marks = str(Marks_Obtained_Number) + "/" + str(Total_Marks_Number)
    pdf.drawString(50, 320, text = "Total Marks :")
    pdf.drawString(135, 320, text = scored_marks)
    Net_Marks = (Marks_Obtained_Number / Total_Marks_Number)*100
    percentage = round(Net_Marks, 2)
    percentage_text = "Total Percentage :  " + str(percentage) + str("%")
    pdf.drawString(50, 300, text = percentage_text)

    if percentage >= 33 :
        pdf.drawString(50, 280, text = "Result :")
        pdf.drawString(105, 280, text = "PASS")
    else:
        pdf.drawString(50, 280, text = "Result :")
        pdf.drawString(105, 280, text = "FAIL")
    
    
    
    marks_row_height = [50,50,50]
    pdf.setDash(10000000,1)
    table = Table(marks_table_data, rowHeights = marks_row_height)
    table.setStyle([ \
    ('GRID', (0,0), (0, -1), 2, colors.black),
    ('GRID', (0, 0), (-1, -1), 0.5 ,colors.black), \
    ('TEXTCOLOR', (0,0), (-1, -1), colors.black), \
    ('ALIGN', (0,0,), (-1, -1), 'CENTER'), \
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), \
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), \
    ('FONTSIZE', (0,0), (-1,-1), 11)])
    
    table.wrapOn(pdf, 100, 400)
    table.drawOn(pdf, 20, 390)

    sign_col_width = [198, 198, 198]
    sign_row_height = [100]
    sign_table = Table(signature_table_data, sign_col_width, sign_row_height)
    sign_table.setStyle([ \
    ('GRID', (0,0), (3,1), 1, colors.black), \
    ('TEXTCOLOR', (0,0), (3, 1), colors.black), \
    ('ALIGN', (0,0), (3,1), 'CENTER'), \
    ('VALIGN', (0,0,), (3, 1), 'TOP'), \
    ('FONTNAME', (0,0), (3,1), 'Helvetica'), \
    ('FONTSIZE', (0,0), (3, 1), 12)])
    
    sign_table.wrapOn(pdf, 100, 400)
    sign_table.drawOn(pdf, 0, 0)

    pdf.save()
    pdflabel = Label(window, text = name_of_file[-1])
    pdflabel.place(x = 1020, y = 425)
    pdf_view_btn['state'] = 'normal'
    print("PDF Report File has been created")
    
def pdf_file_viewer():
    os.startfile(updated_pdf_path)

def adminpassmenu():
    def admpasscheck():
        cur.execute('SELECT Password FROM admin;')
        pwd = (cur.fetchone()[0]).encode()
        userpass = admpassentry.get()
        print(userpass)
        if bcrypt.checkpw((userpass.encode()), pwd) is True:
            adminpassmenu.destroy()
            adminmode()
        else:
            admin_try_lbl = Label(adminpassmenu, text="Try again", fg="#fb3934", font=('Tw Cen MT', 11))
            admin_try_lbl.place(relx=0.5, rely=0.85, anchor='center')                

    adminpassmenu = Tk()
    defaultFont = font.nametofont("TkDefaultFont")
    defaultFont.configure(family="Tw Cen MT", size=13)
    adminpassmenu.title('Admin Login')
    adminpassmenu.iconbitmap(os.path.join(cwd,'assets/admin.ico'))
    adminpassmenu.geometry("410x300")
    adminpassmenu.tk_setPalette(background="#282828", foreground="#ebdbb2")
    adminpassmenu.resizable(0, 0)
    bg = "#282828"
    fg = "#ebdbb2"
    graybox = "#a89984"

    admlogin_lbl = Label(adminpassmenu, text="Admin Login", fg = "#b8bb26", font = ("Bahnschrift",30))
    admlogin_lbl.place(relx=0.5, rely=0.1, anchor="center")

    enteradmpass_lbl = Label(adminpassmenu, text="Enter Admin Password", justify='center')
    enteradmpass_lbl.place(relx=0.5, rely=0.4, anchor='center')

    useradmpass = StringVar()
    admpassentry = Entry(adminpassmenu, textvariable=useradmpass, selectbackground=fg, selectforeground=bg, justify='center', show='*')
    admpassentry.place(relx=0.5,rely=0.55, anchor='center')

    admsubmit = Button(adminpassmenu, text="Login", command=admpasscheck)
    admsubmit.place(relx=0.5, rely=0.7, anchor='center')

    adminpassmenu.mainloop()

def adminmode():

    # Functions #

    def sch_add():
        def close():
            popup.destroy()

        school = schooltxt.get()
        
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
        
        schooldrop['menu'].delete(0, 'end')
        for sch in packages.functions.schoollist:
            schoolcmd = tkinter._setit(schoolvar, sch)
            schooldrop['menu'].add_command(label=sch, command=schoolcmd)
        schoolvar.set([str(i).strip("}{(,)'") for i in packages.functions.schoollist][0])

    def sch_delete():
        def close():
            popupwarn.destroy()
        
        def confirm():
            school = schooltxt.get()
            try:
                cur.execute('DELETE FROM student WHERE SchoolName = "'+str(school)+'";')
                cur.execute('DELETE FROM schools WHERE Name = "'+str(school)+'";')
                packages.functions.db.commit()
                schooltree.delete(*schooltree.get_children())
                packages.functions.master_lists()
                for i in packages.functions.schoollist:
                    schooltree.insert('','end',values=(i))
                
                schooldrop['menu'].delete(0, 'end')
                for sch in packages.functions.schoollist:
                    schoolcmd = tkinter._setit(schoolvar, sch)
                    schooldrop['menu'].add_command(label=sch, command=schoolcmd)
                schoolvar.set([str(i).strip("}{(,)'") for i in packages.functions.schoollist][0])          
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
        def close():
            popup.destroy()

        classname = classtxt.get()
        
        try:
            cur.execute("USE report_card_db;")
        
            cur.execute('INSERT INTO class (Name) \
                VALUES ("'+str(classname)+'");')
            packages.functions.db.commit()
        except:
            popup = Tk()
            popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
            popup.geometry("255x150+572+340")
            popup.title("Error!")
            popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

            error = Label(popup, text="Class already exists", font=("Bahnschrift", 17), fg="#fb4934")
            error.place(x=8,y=25)

            okbutton = Button(popup, text="Ok", command=close, width=10)
            okbutton.place(x=85,y=90)
        
        classtree.delete(*classtree.get_children())
        packages.functions.master_lists()
        for i in packages.functions.classlist:
            classtree.insert('','end',values=(i))
        
        classvar.set("None")
        classdrop['menu'].delete(0, 'end')
        for c in packages.functions.classlist:
            classcmd = tkinter._setit(classvar, c)
            classdrop['menu'].add_command(label=c, command=classcmd)

    def class_delete():
        def close():
            popupwarn.destroy()
        
        def confirm():
            classname = classtxt.get()
            try:
                
                cur.execute('DELETE FROM class WHERE Name = "'+str(classname)+'";')
                packages.functions.db.commit()
                classtree.delete(*classtree.get_children())
                packages.functions.master_lists()
                for i in packages.functions.classlist:
                    classtree.insert('','end',values=(i))
                classvar.set("None")
                classdrop['menu'].delete(0, 'end')
                for c in packages.functions.classlist:
                    classcmd = tkinter._setit(classvar, c)
                    classdrop['menu'].add_command(label=c, command=classcmd)
                    
            except:
                pass
            popupwarn.destroy()

        popupwarn = Tk()  

        popupwarn.iconbitmap(os.path.join(cwd,"assets/confirm.ico"))
        popupwarn.geometry("255x150+572+340")
        popupwarn.title("Confirmation")
        popupwarn.tk_setPalette(background="#282828", foreground="#ebdbb2")

        warninglbl = Label(popupwarn, text="Are you sure?\nThis will delete ALL\ndata for the class", font=("Bahnschrift", 14), fg="#fb4934")
        warninglbl.place(relx=0.5,rely=0.3, anchor=CENTER)

        okbutton = Button(popupwarn, text="Confirm", command=confirm, width=10)
        okbutton.place(relx=0.7,rely=0.7, anchor=CENTER)

        cnclbutton = Button(popupwarn, text="Cancel", command=close,width=10)
        cnclbutton.place(relx=0.3,rely=0.7, anchor=CENTER)
        popupwarn.mainloop()

    def section_add():
        def close():
            popup.destroy()

        sectionname = sectiontxt.get()
        
        try:
            cur.execute("USE report_card_db;")
        
            cur.execute('INSERT INTO sections (Name) \
                VALUES ("'+str(sectionname)+'");')
            packages.functions.db.commit()
        except:
            popup = Tk()
            popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
            popup.geometry("255x150+572+340")
            popup.title("Error!")
            popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

            error = Label(popup, text="Section already exists", font=("Bahnschrift", 17), fg="#fb4934")
            error.place(x=8,y=25)

            okbutton = Button(popup, text="Ok", command=close, width=10)
            okbutton.place(x=85,y=90)
        
        sectiontree.delete(*sectiontree.get_children())
        packages.functions.master_lists()
        for i in packages.functions.sectionlist:
            sectiontree.insert('','end',values=(i))
        sectionvar.set("None")
        sectiondrop['menu'].delete(0, 'end')
        for s in packages.functions.sectionlist:
            sectioncmd = tkinter._setit(sectionvar, s)
            sectiondrop['menu'].add_command(label=s, command=sectioncmd)

    def section_delete():
        def close():
            popupwarn.destroy()
        
        def confirm():
            sectionname = sectiontxt.get()
            try:
                cur.execute('DELETE FROM sections WHERE Name = "'+str(sectionname)+'";')
                packages.functions.db.commit()
                sectiontree.delete(*sectiontree.get_children())
                packages.functions.master_lists()
                for i in packages.functions.sectionlist:
                    sectiontree.insert('','end',values=(i))
                sectionvar.set("None")
                sectiondrop['menu'].delete(0, 'end')
                for s in packages.functions.sectionlist:
                    sectioncmd = tkinter._setit(sectionvar, s)
                    sectiondrop['menu'].add_command(label=s, command=sectioncmd)
                    
            except:
                pass
            popupwarn.destroy()

        popupwarn = Tk()  

        popupwarn.iconbitmap(os.path.join(cwd,"assets/confirm.ico"))
        popupwarn.geometry("255x150+572+340")
        popupwarn.title("Confirmation")
        popupwarn.tk_setPalette(background="#282828", foreground="#ebdbb2")

        warninglbl = Label(popupwarn, text="Are you sure?\nThis will delete ALL\ndata for the Section", font=("Bahnschrift", 14), fg="#fb4934")
        warninglbl.place(relx=0.5,rely=0.3, anchor=CENTER)

        okbutton = Button(popupwarn, text="Confirm", command=confirm, width=10)
        okbutton.place(relx=0.7,rely=0.7, anchor=CENTER)

        cnclbutton = Button(popupwarn, text="Cancel", command=close,width=10)
        cnclbutton.place(relx=0.3,rely=0.7, anchor=CENTER)
        popupwarn.mainloop()

    def sub_add():
        def close():
            popup.destroy()

        subjectname = subtxt.get()
        
        try:
            cur.execute("USE report_card_db;")
        
            cur.execute('INSERT INTO subjects (Name) \
                VALUES ("'+str(subjectname)+'");')
            packages.functions.db.commit()
        except:
            popup = Tk()
            popup.iconbitmap(os.path.join(cwd,"assets/error.ico"))
            popup.geometry("255x150+572+340")
            popup.title("Error!")
            popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

            error = Label(popup, text="Subject already exists", font=("Bahnschrift", 17), fg="#fb4934")
            error.place(x=8,y=25)

            okbutton = Button(popup, text="Ok", command=close, width=10)
            okbutton.place(x=85,y=90)
        
        subtree.delete(*subtree.get_children())
        packages.functions.master_lists()
        for i in packages.functions.sublist:
            subtree.insert('','end',values=(i))
        subvar.set("None")
        subject_drop['menu'].delete(0, 'end')
        for su in packages.functions.sublist:
            subcmd = tkinter._setit(subvar, su)
            subject_drop['menu'].add_command(label=su, command=subcmd)

    def sub_delete():
        def close():
            popupwarn.destroy()
        
        def confirm():
            subjectname = subtxt.get()
            try:
                
                cur.execute('DELETE FROM subjects WHERE Name = "'+str(subjectname)+'";')
                packages.functions.db.commit()
                subtree.delete(*subtree.get_children())
                packages.functions.master_lists()
                for i in packages.functions.sublist:
                    subtree.insert('','end',values=(i))
                subvar.set("None")
                subject_drop['menu'].delete(0, 'end')
                for su in packages.functions.sublist:
                    subcmd = tkinter._setit(subvar, su)
                    subject_drop['menu'].add_command(label=su, command=subcmd)
                    
            except:
                pass
            popupwarn.destroy()

        popupwarn = Tk()  

        popupwarn.iconbitmap(os.path.join(cwd,"assets/confirm.ico"))
        popupwarn.geometry("255x150+572+340")
        popupwarn.title("Confirmation")
        popupwarn.tk_setPalette(background="#282828", foreground="#ebdbb2")

        warninglbl = Label(popupwarn, text="Are you sure?\nThis will delete ALL\ndata for the Subject", font=("Bahnschrift", 14), fg="#fb4934")
        warninglbl.place(relx=0.5,rely=0.3, anchor=CENTER)

        okbutton = Button(popupwarn, text="Confirm", command=confirm, width=10)
        okbutton.place(relx=0.7,rely=0.7, anchor=CENTER)

        cnclbutton = Button(popupwarn, text="Cancel", command=close,width=10)
        cnclbutton.place(relx=0.3,rely=0.7, anchor=CENTER)
        popupwarn.mainloop()

    def sch_fetch(event):
        schItem = schooltree.focus()
        schvalues = schooltree.item(schItem)
        schooltxt.delete(0, END)
        schooltxt.insert(0, schvalues['values'][0])

    def c_fetch(event):
        classItem = classtree.focus()
        classvalues = classtree.item(classItem)
        classtxt.delete(0, END)
        classtxt.insert(0, classvalues['values'][0])

    def sec_fetch(event):
        secItem = sectiontree.focus()
        secvalues = sectiontree.item(secItem)
        sectiontxt.delete(0, END)
        sectiontxt.insert(0, secvalues['values'][0])
    
    def sub_fetch(event):
        subItem = subtree.focus()
        subvalues = subtree.item(subItem)
        subtxt.delete(0, END)
        subtxt.insert(0, subvalues['values'][0])

    # Initialization #

    admin = Tk()

    packages.functions.master_lists()
    cwd = os.path.dirname(os.path.abspath(__file__))

    admincanvas = Canvas(admin)
    admincanvas.config(width='920', height='450')
    line1 = admincanvas.create_line(230,50,230,768, fill='#458588', width=2)
    line2 = admincanvas.create_line(462,50,462,768, fill='#458588', width=2)
    line3 = admincanvas.create_line(694,50,694,768, fill='#458588', width=2)
    line4 = admincanvas.create_line(0,50,1366,50, fill='#fb4934', width=3)
    admincanvas.pack()

    defaultFont = font.nametofont("TkDefaultFont")
    defaultFont.configure(family="Tw Cen MT", size=13)
    admin.title('Admin')
    admin.iconbitmap(os.path.join(cwd,'assets/admin.ico'))
    admin.geometry("920x450")
    admin.tk_setPalette(background="#282828", foreground="#ebdbb2")
    admin.resizable(0, 0)

    title = Label(admin, text="Admin Mode", fg = "#b8bb26", font = ("Bahnschrift",30))
    title.place(relx=0.5, rely=0.1, anchor=CENTER)

    # Schools #

    schools = Label(admin, text="Schools", fg=fg, font=("Bahnschrift",23))
    schools.place(relx=0.125, rely=0.2, anchor=CENTER)
    
    schooltxt = Entry(admin, text="", selectbackground=fg, selectforeground=bg, justify='center', width=30)
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
    
    schooltree.bind("<ButtonRelease-1>", sch_fetch)
    # Classes #

    classes = Label(admin, text="Classes", fg=fg, font=("Bahnschrift",23))
    classes.place(relx=0.378, rely=0.2, anchor=CENTER)

    classtxt = Entry(admin, text="", selectbackground=fg, selectforeground=bg, justify='center', width=30)
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

    classtree.bind("<ButtonRelease-1>", c_fetch)

    # Sections #

    sections = Label(admin, text="Sections", fg=fg, font=("Bahnschrift",23))
    sections.place(relx=0.631, rely=0.2, anchor=CENTER)

    sectiontxt = Entry(admin, text="", selectbackground=fg, selectforeground=bg, justify='center', width=30)
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
    
    sectiontree.bind("<ButtonRelease-1>", sec_fetch)

    # Subjects #

    subjects = Label(admin, text="Subjects", fg=fg, font=("Bahnschrift",23))
    subjects.place(relx=0.880, rely=0.2, anchor=CENTER)

    asubvar = StringVar()
    subtxt = Entry(admin, textvariable=asubvar, selectbackground=fg, selectforeground=bg, justify='center', width=30)
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
    
    subtree.bind("<ButtonRelease-1>", sub_fetch)

    admin.mainloop()

def examchng(x):
    sItem = stutree.focus()
    svalues = stutree.item(sItem)
    print("Affirmative")
    cur.execute('SELECT StudentID FROM student WHERE AdmissionNo = "'+str(svalues['values'][0])+'";')
    s_id = str(cur.fetchone()).strip('(,)')

    print(s_id)
    cur.execute('SELECT DISTINCT e.Name FROM exam e INNER JOIN academics a ON a.AcademicID = e.AcademicID INNER JOIN student s ON s.StudentID = a.StudentID WHERE s.StudentID = "'+str(s_id)+'"AND a.Year = "'+str(yeardropvar.get())+'";')
    
    global examlist
    examlist = []
    for i in cur.fetchall():
        examlist.append(str(i).strip("(,)'"))

    examdrop['menu'].delete(0, 'end')
    for e in examlist:
        examcmd = tkinter._setit(examdropvar, e)
        examdrop['menu'].add_command(label=e, command=examcmd)

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

pdf_lbl = Label(window, text="Generate PDF", font = ("Bahnschrift",20))
pdf_lbl.place(x = 1010, y = 100) 

## STUDENT INFO ##
# School Name
school_lbl = Label(window, text = "School Name")
school_lbl.place(x = 65, y = 150)
schoolvar = StringVar()
schoolvar.set([str(i).strip("}{(,)'") for i in packages.functions.schoollist][0])
schooldrop = OptionMenu(window, schoolvar, *[str(i).strip("}{(,)'") for i in packages.functions.schoollist])
schooldrop.place(x = 165, y = 147)

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
update_btn = Button(window, text = "Update", command = s_update, width=7, fg="#83a598")
update_btn.place(x = 60, y = 400)

addstudent_btn = Button(window, text = "Add", command = studentsubmit, width=7, fg="#b8bb26")
addstudent_btn.place(x=140,y = 400)

delstudent_btn = Button(window, text = "Delete", command=s_delete, width=7, fg="#fb4934")
delstudent_btn.place(x=220, y = 400)

## ADDING/EDITING EXAM RESULTS ##

class_lbl = Label(window, text = "Class")
class_lbl.place(x = 415, y = 203)

classvar= StringVar()
classvar.set("None")
classdrop = OptionMenu(window, classvar, *[str(i).strip("}{(,)'") for i in packages.functions.classlist])
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
sectiondrop = OptionMenu(window,sectionvar,*[str(i).strip("}{(,)'") for i in packages.functions.sectionlist])
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
subject_drop = OptionMenu(window, subvar, *[str(i).strip("}{(,)'") for i in packages.functions.sublist])
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

admin_mode = Button(window, text="Admin Mode", command=adminpassmenu, width=15)
admin_mode.place(relx=0.5, rely=0.955, anchor=CENTER)

# Generating PDF

pdf_gen_btn = Button(window, text = "Create PDF", command = pdf_gen)
pdf_gen_btn.place(x=1050, y=300)

yeardrop_lbl = Label(window, text="Year", font=('Tw Cen MT', 12))
yeardrop_lbl.place(x=1025, y=205)

yeardropvar = StringVar()
yeardropvar.set("None")
yearlist = ['']
yeardrop = OptionMenu(window, yeardropvar, *[str(i).strip("}{(,)'") for i in yearlist], command=examchng)
yeardrop.place(x=1070, y=200)

examdrop_lbl = Label(window, text='Exam', font=('Tw Cen MT', 12))
examdrop_lbl.place(x=1025,y=245)

examdropvar = StringVar()
examdropvar.set('None')
examlist = ['']
examdrop = OptionMenu(window, examdropvar, *[str(i).strip("}{(,)'") for i in examlist])
examdrop.place(x=1070, y=240)

# PDF Viewer

#initial_pdf_lbl = Label(window, text = "Open PDF -> ")
#initial_pdf_lbl.place(x = 950, y = 365)
pdfimg = PhotoImage(file = os.path.join(cwd,'assets/pdf.png'))   
pdf_view_btn = Button(window, image = pdfimg, command = lambda : pdf_file_viewer(), borderwidth=0)
pdf_view_btn.place(x = 1077, y = 360)

pdf_view_btn['state'] = 'disable'

window.mainloop()
