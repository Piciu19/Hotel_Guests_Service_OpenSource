from configparser import ConfigParser
import os
import postgresConnectionLibrary
import maskpass

hostname = None
db = None
username = None
pwd = None
port = None
def postgresServerConfiguration():
    global hostname
    global db
    global username
    global pwd
    global port
    cfgObject = ConfigParser()
    try:
        if not os.path.exists('config.cfg'):
            print('Please set up informations for PostgreSQL server:')
            hostname = str(input('Enter hostname: '))
            db = str(input('Enter database name: '))
            username = str(input('Enter username: '))
            pwd = maskpass.askpass(prompt='Enter password: ', mask='*')
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

            createSchemaScript = f'CREATE SCHEMA IF NOT EXISTS hotel AUTHORIZATION {username};'

            createTableScript = '''CREATE TABLE IF NOT EXISTS hotel.guests
                                    (
                                        id serial PRIMARY KEY,
                                        name text,
                                        last_name text,
                                        phone integer,
                                        number_of_guests integer,
                                        room_number integer
                                    )'''
            postgresConnection = postgresConnectionLibrary.PostgressConnection(hostname, db, username, pwd, port)
            postgresConnection.schemaTable(createSchemaScript, createTableScript)
            del postgresConnection
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

def addGuest():
    while True:
        try:
            name = input("Enter guest name: ")
            if name.isdigit() == True:
                raise Exception
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    while True:
        try:
            lastName = input("Enter guest last name: ")
            if lastName.isdigit() == True:
                raise Exception
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    while True:
        try:
            phone = int(input("Enter guest phone: "))
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    while True:
        try:
            numberOfGuests = int(input("Enter number of guests: "))
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    while True:
        try:
            roomNumber = int(input("Enter number of room: "))
            break
        except Exception:
            print("Entered data is incorrect. Try again")
            continue

    print(f'Name : {name}\nLast Name : {lastName}\nPhone : {phone}\nNumber of guests : {numberOfGuests}\nRoom number : {roomNumber}')

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
        addGuestScript = f'INSERT INTO hotel.guests (name,last_name,phone,number_of_guests,room_number) VALUES (%s,%s,%s,%s,%s)'
        addGuestValue = (name,lastName,phone,numberOfGuests,roomNumber)
        postgresConnection.add(addGuestScript,addGuestValue)
    elif sure == 0:
        print("Guest not added")


def viewGuestsList():
    fetchScript = 'SELECT * FROM hotel.guests'
    postgresConnection.view(fetchScript)

def deleteGuest():
    viewGuestsList()
    id = input('Enter guest id you want to delete: ')
    deleteScript = 'DELETE FROM hotel.guests WHERE id =%s'
    deleteID = (id)
    postgresConnection.delete(deleteScript,deleteID)

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
    postgresServerConfiguration()
    postgresConnection = postgresConnectionLibrary.PostgressConnection(hostname, db, username, pwd, port)
    choicesFunc()
    print()

    if choice == 1:
        addGuest()
    elif choice == 2:
        deleteGuest()
    elif choice == 3:
        viewGuestsList()
    elif choice == 4:
        schemaDrop = 'DROP SCHEMA IF EXISTS hotel;'
        tableDrop = 'DROP TABLE IF EXISTS hotel.guests;'
        postgresConnection.schemaTable(tableDrop, schemaDrop)
        os.remove('config.cfg')
        del postgresConnection
        postgresServerConfiguration()
    else:
        print("Entered data is incorrect. try again")