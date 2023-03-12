from configparser import ConfigParser
import os
import postgresConnectionLibrary
import maskpass
import logging
import datetime
import time

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
            logging.info('execute pre-configuration')
            print('Pre-configuration for postgres database')
            print('After you enter data program will create schema and table in database')
            print()
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

            try:
                with open('config.cfg', "w") as f:
                    print()
                    print(f'hostname : {hostname}\ndb name : {db}\nusername : {username}\npassword : {pwd}\nport : {port}')
                    print('If entered values are incorrect enter 4')
                    cfgObject.write(f)
                    logging.info(f'New config created (hostname : {hostname}, db name : {db}, username : {username}, password : {pwd}, port : {port})')
            except Exception as error:
                logging.error(error)
                print(error)

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
            logging.info(f'New schema and table created in database {db}')
        else:
            cfgObject.read('config.cfg')
            postgresinfo = cfgObject['PostgresServerConnInfo']

            hostname = postgresinfo['hostname']
            db = postgresinfo['db']
            username = postgresinfo['username']
            pwd = postgresinfo['pwd']
            port = postgresinfo['port']
            logging.info('Config read successfully')

    except Exception as error:
        logging.error(error)

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
        try:
            addGuestScript = f'INSERT INTO hotel.guests (name,last_name,phone,number_of_guests,room_number) VALUES (%s,%s,%s,%s,%s)'
            addGuestValue = (name,lastName,phone,numberOfGuests,roomNumber)
            postgresConnection.add(addGuestScript,addGuestValue)
            logging.info('Added new guest\nName : {name}\nLast Name : {lastName}\nPhone : {phone}\nNumber of guests : {numberOfGuests}\nRoom number : {roomNumber}')
        except Exception as error:
            print(error)
            logging.error(error)
    elif sure == 0:
        print("Guest not added")
        logging.info('Guest added canceled')


def viewGuestsList():
    try:
        fetchScript = 'SELECT * FROM hotel.guests'
        postgresConnection.view(fetchScript)
        logging.info('Guests list fetch')
    except Exception as error:
        print(error)
        logging.error(error)

def deleteGuest():
    try:
        viewGuestsList()
        id = input('Enter guest id you want to delete: ')
        deleteScript = 'DELETE FROM hotel.guests WHERE id =%s'
        deleteID = (id)
        postgresConnection.delete(deleteScript,deleteID)
        logging.info('Deleted guest')
    except Exception as error:
        print(error)
        logging.error(error)

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
logging.basicConfig(filename=f'.log', filemode='a', format='[%(asctime)s %(levelname)s] %(message)s', level=logging.INFO)
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