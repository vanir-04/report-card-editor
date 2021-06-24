import mysql.connector
import getpass

# Ask for password

askpwd = 0

while askpwd == 0:
    pwd = getpass.getpass('Please enter your password: ')
    try:
        db = mysql.connector.connect(host='localhost', user='root', password=pwd)
        askpwd = 1
    except:
        print("Try again.")

# Create cursors

cur = db.cursor(buffered=True)
cur2 = db.cursor()

# Check for existence of database and create it if not found

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
    cur.execute("USE report_card_db;")

# Check for existence of tables and create them if not found

cur.execute("SHOW TABLES;")
cur2.execute("USE report_card_db;")

sub_exist = False
class_exist = False
stu_exist = False
aca_exist = False
exam_exist = False

for i in cur:
    if 'subjects' in i:
        sub_exist = True    
    elif 'class' in i:
        class_exist = True
    elif 'student' in i:
        stu_exist = True
    elif 'academics' in i:
        aca_exist = True
    elif 'exam' in i:
        exam_exist = True
    else:
        continue

y = 0

while y <= 4:
    if sub_exist != True:
        print("Subjects table not found, creating...")
        cur2.execute("CREATE TABLE subjects(SubjectID int AUTO_INCREMENT, Name varchar(255), PRIMARY KEY (SubjectID));")
        print("Subjects table created.")
        sub_exist = True
        y = y + 1
    elif class_exist != True:
        print("Class table not found, creating...")
        cur2.execute("CREATE TABLE class(ClassID int, Name varchar(255));")
        print("Class table created.")
        class_exist = True
        y = y + 1
    elif stu_exist != True:
        print("Student table not found, creating...")
        cur2.execute("CREATE TABLE student(StudentID int AUTO_INCREMENT, AdmissionNo varchar(255), Name varchar(255), DOB date, PRIMARY KEY (StudentID));")
        print("Student table created.")
        stu_exist = True
        y = y + 1
    elif aca_exist != True:
        print("Academics table not found, creating...")
        cur2.execute("CREATE TABLE academics(AcademicID int AUTO_INCREMENT, StudentID int, ClassID int, SubjectID int, RollNo int, PRIMARY KEY (AcademicID));")
        print("Academics table created.")
        aca_exist = True
        y = y + 1
    elif exam_exist != True:
        print("Exam table not found, creating...")
        cur2.execute("CREATE TABLE exam(AcademicID int, Name varchar(255), TotalMarks int, MarksObtained int, Date date);")
        print("Exam table created.")
        exam_exist = True
        y = y + 1
    else:
        print("All tables found.")
        break
else:
    print("All tables found.")



