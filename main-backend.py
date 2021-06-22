import mysql.connector
import getpass

askpwd = 0

while askpwd == 0:
    pwd = getpass.getpass('Please enter your password: ')
    try:
        db = mysql.connector.connect(host='localhost', user='root', password=pwd)
        askpwd = 1
    except:
        print("Try again.")

cur = db.cursor(buffered=True)
cur2 = db.cursor()

cur.execute("SHOW DATABASES;")

db_exist = False

for x in cur:
    if 'report_card_db' in x:
        db_exist = True
        break
    else:
        db_exist = False

if db_exist == True:
    print("Database found!")
    cur.execute("USE report_card_db;")
else:
    print("Database doesn't exist. Creating...")
    cur.execute("CREATE DATABASE report_card_db;")
    print("Database Created!")

cur.execute("SHOW TABLES;")
y=0

for i in cur:
    cur.execute("SHOW TABLES;")
    print("YEAH")
    while y <= 4:
        if 'subject' not in i and y == 0:
            print("Subjects table not found, creating...")
            cur2.execute("CREATE TABLE subject(SubjectID int, Name varchar(255), Description varchar(255));")
            print("Subjects table created.")
            y = y+1
        elif 'class' not in i and y == 1:
            print("Class table not found, creating...")
            cur2.execute("CREATE TABLE class(ClassID int, Name varchar(255));")
            print("Class table created.")
            y = y+1
        elif 'student' not in i and y == 2:
            print("Student table not found, creating...")
            cur2.execute("CREATE TABLE student(StudentID int, AdmissionNo varchar(255), Name varchar(255), DOB date);")
            print("Student table created.")
            y = y+1
        elif 'academics' not in i and y == 3:
            print("Academics table not found, creating...")
            cur2.execute("CREATE TABLE academics(AcademicID int, StudentID int, ClassID int, SubjectID int, RollNo int);")
            print("Academics table created.")
            y = y+1
        elif 'exam' not in i and y == 4:
            print("Exam table not found, creating...")
            cur2.execute("CREATE TABLE exam(AcademicID int, Name varchar(255), TotalMarks int, MarksObtained int, Date date);")
            print("Exam table created.")
            y = y+1
        else:
            print("All tables found.")
            y = 5


    
    
    