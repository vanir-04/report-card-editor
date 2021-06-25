from tkinter import *
import packages.functions

#packages.functions.login()
packages.functions.cli_login()

# Create cursors

cur = packages.functions.db.cursor(buffered=True)
cur2 = packages.functions.db.cursor()

# Check for existence of database and create it if not found

cur.execute("SHOW DATABASES;")

db_exist = False
sub_exist, class_exist, stu_exist, aca_exist, exam_exist, section_exist = False, False, False, False, False, False

for i in cur:
    if 'report_card_db' in i:
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
    elif 'sections' in i:
        section_exist = True
    else:
        continue

y = 0

while y <= 5:
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
        cur2.execute("CREATE TABLE student(StudentID int AUTO_INCREMENT, AdmissionNo varchar(255), Name varchar(255), RollNo int, Gender varchar(255), PRIMARY KEY (StudentID));")
        print("Student table created.")
        stu_exist = True
        y = y + 1
    elif aca_exist != True:
        print("Academics table not found, creating...")
        cur2.execute("CREATE TABLE academics(AcademicID int AUTO_INCREMENT, StudentID int, ClassID int, SubjectID int, PRIMARY KEY (AcademicID));")
        print("Academics table created.")
        aca_exist = True
        y = y + 1
    elif exam_exist != True:
        print("Exam table not found, creating...")
        cur2.execute("CREATE TABLE exam(AcademicID int, Name varchar(255), TotalMarks int, MarksObtained int, Date date);")
        print("Exam table created.")
        exam_exist = True
        y = y + 1
    elif section_exist != True:
        print("Sections table not found, creating...")
        cur2.execute("CREATE TABLE sections(SectionID int AUTO_INCREMENT, Name varchar(255), PRIMARY KEY (SectionID));")
        print("Sections table created.")
        section_exist = True
    else:
        print("All tables found.")
        break
else:
    print("All tables found.")

# Add pre-existing data to the tables

cur2.execute("DELETE FROM subjects;")
cur2.execute("ALTER TABLE subjects AUTO_INCREMENT = 1;")
cur2.execute("INSERT INTO subjects (Name)\
    VALUES \
        ('Accountancy'),\
        ('Biology'),\
        ('Business Studies'),\
        ('Chemistry'),\
        ('Commercial Arts'),\
        ('Economics'),\
        ('English'),\
        ('Geography'),\
        ('History'),\
        ('Maths'),\
        ('Physical Education'),\
        ('Physics'),\
        ('Political Science'),\
        ('Psychology'),\
        ('Informatics Practices'),\
        ('Computer Science');")

cur2.execute("DELETE FROM class;")
cur2.execute("INSERT INTO class (ClassID, Name)\
    VALUES \
        (11, 'XI'),\
        (12, 'XII');")

cur2.execute("DELETE FROM sections;")
cur2.execute("INSERT INTO sections (Name)\
    VALUES \
        ('A'),\
        ('B'),\
        ('C'),\
        ('D'),\
        ('E'),\
        ('F'),\
        ('G');")

packages.functions.db.commit()