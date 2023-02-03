import json
import psycopg2
from configparser import ConfigParser
import os

# Functions
global isFirstStart
def postgresInfo():
    cfgObject = ConfigParser()

    global hostname
    global db
    global username
    global pwd
    global port

    try:
        if not os.path.exists('config.cfg'):
            print('Please set up informations for PostgreSQL server:')
            hostname = str(input('Enter hostname: '))
            db = str(input('Enter database name: '))
            username = str(input('Enter username: '))
            pwd = str(input('Enter password: '))
            port = str(input('Enter port:'))

            cfgObject['PostgresServerConnInfo'] = {}
            config = cfgObject['PostgresServerConnInfo']
            config['hostname'] = hostname
            config['db'] = db
            config['username'] = username
            config['pwd'] = pwd
            config['port'] = port

            with open('config.cfg', "w") as f:
                cfgObject.write(f)
        else:
            cfgObject.read('config.cfg')
            postgresinfo = cfgObject['PostgresServerConnInfo']

            hostname = postgresinfo['hostname']
            db = postgresinfo['db']
            username = postgresinfo['username']
            pwd = postgresinfo['pwd']
            port = postgresinfo['port']


    except Exception as error:
        print(error)
def postgresConnection():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = db,
            user = username,
            password = pwd,
            port = port)

        cur = conn.cursor()

        getScript = '''SELECT * FROM "Hotel_guests_list"."Guests"'''
        cur.execute(getScript)

    except Exception as error:
        print(error)

    cur.close()
    conn.close()

def addGuest():
    global sure
    guestData = {}
    while True:
        try:
            guestData["name"] = input("Enter guest name: ")
            if guestData["name"].isdigit() == True:
                raise Exception
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    while True:
        try:
            guestData["last name"] = input("Enter guest last name: ")
            if guestData["last name"].isdigit() == True:
                raise Exception
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    while True:
        try:
            guestData["phone"] = int(input("Enter guest phone: "))
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    while True:
        try:
            guestData["number of guests"] = int(input("Enter number of guests: "))
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    while True:
        try:
            guestData["room number"] = int(input("Enter number of room: "))
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    print(guestData)

    print("[1] - yes")
    print("[0] - no")
    while True:
        try:
            sure = int(input("Are you sure to add new guest? "))
            if sure != 1 and sure != 0:
                raise Exception
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    if sure == 1:
        try:
            with open("guests_list.json", "r") as f:
                temp = json.load(f)
            temp.append(guestData)
            with open("guests_list.json", "w") as f:
                json.dump(temp, f, indent=4)
            print("Guest successful added")
        except Exception:
            print("Problem with add guest, try again")
    elif sure == 0:
        print("Guest not added")


def viewGuestsList():
    pass


def deleteGuest():
    viewGuestsList()
    new_data = []
    with open("guests_list.json", "r") as f:
        temp = json.load(f)
        data_length = len(temp)
    print("Which guest number do you like to delete?")
    while True:
        try:
            deleteOption = input(f"Select a number 0-{data_length - 1}: ")
            delOptRange = range(0, int(data_length))
            if int(deleteOption) in delOptRange:
                print("Guest successfully deleted")
                break
            else:
                print("Entered data is incorrect. Try again")
        except Exception:
            print("That not a number")
    i = 0
    for entry in temp:
        if i == int(deleteOption):
            pass
            i = i + 1
        else:
            new_data.append(entry)
            i = i + 1
        with open("guests_list.json", "w") as f:
            json.dump(new_data, f, indent=4)

def modeChoiceCheck():
    if choice != 1 and choice != 2 and choice != 3 and choice != 4:
        raise Exception

def choicesFunc():
    global choice
    print("----------------------------------------------------------------------------")
    print("[1] - Add guest")
    print("[2] - Delete guest")
    print("[3] - View guests list")
    print("[4] - Change postgres info")
    try:
        choice = int(input("Enter number: "))
        modeChoiceCheck()
    except Exception:
        print("Entered data is incorrect")


# Program
while True:
    postgresInfo()
    print(hostname, db, username, pwd, port)
    choicesFunc()
    print()

    if choice == 1:
        addGuest()
    elif choice == 2:
        deleteGuest()
    elif choice == 3:
        viewGuestsList()
    elif choice == 4:
        os.remove('config.cfg')
        postgresInfo()
    else:
        print("Entered data is incorrect. try again")
