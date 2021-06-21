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