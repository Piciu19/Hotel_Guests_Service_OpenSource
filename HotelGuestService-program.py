import json
#Functions
def modeChoiceCheck(choice):
    if (choice != 1 and choice != 2 and choice != 3 and choice != 4):
        raise Exception 

def addGuest():
    guestData = {}
    while True:
        try:
            guestData["Name"] = input("Enter guest name: ")
            if (guestData["Name"].isdigit() == True):
                raise Exception
            break
        except Exception:
            print("Entred data is incorrect. Try again")
            continue
        
    while True:
        try:
            guestData["Last name"] = input("Enter guest last name: ")
            if (guestData["Last name"].isdigit() == True):
                raise Exception
            break
        except Exception:
            print("Entred data is incorrect. Try again")
            continue
    
    while True:
        try:
            guestData["Phone"] = int(input("Enter guest phone: "))
            break
        except Exception:
            print("Entred data is incorrect. Try again")
            continue
    
    while True:
        try:
            guestData["Peoples in the room"] = int(input("Enter number of peoples in the room: "))
            break
        except Exception:
            print("Entred data is incorrect. Try again")
            continue
    
    while True:
        try:
            guestData["Number of the room"] = int(input("Enter number of room: "))
            break
        except Exception:
            print("Entred data is incorrect. Try again")
            continue
           
    print(guestData)

    print("[1] - yes")
    print("[0] - no")
    while True:
        try:
            sure = int(input("Are you sure to add new guest? "))
            if (sure != 1 and sure != 0):
                raise Exception
            break
        except Exception:
                print("Entred data is incorrect. Try again")
                continue

    if (sure == 1):
        try:
            with open("guests_list.json", "r") as f:
                temp = json.load(f)
            temp.append(guestData)
            with open("guests_list.json", "w") as f:
                json.dump(temp, f, indent=4)
            print("Guest successful added")
        except Exception:
            print("Problem with add guest, try again")
    elif (sure == 0):
        print("Guest not added")

def viewGuestsList():
    with open("guests_list.json") as f:
        jsonF = json.load(f)
        i = 0
        for guests in jsonF:
            name = guests["Name"]
            lastName = guests["Last name"]
            phone = guests["Phone"]
            peoplesInRoom = guests["Peoples in the room"]
            numOfRoom = guests["Number of the room"]
            print(f"Index : {i}")
            print(f"Name : {name} | " + f"Last name : {lastName} | " + f"Phone : {phone} | " + f"Peoples in the room : {peoplesInRoom} | " + f"Number of the room : {numOfRoom}")
            print()

            i = i+1


def deleteGuest():
    viewGuestsList()
    new_data = []
    with open("guests_list.json", "r") as f:
        temp = json.load(f)
        data_legnth = len(temp)
    print("Wich guest number do you like to delete?")
    while True:
        try:
            deleteOption = input(f"Select a number 0-{data_legnth-1}: ")
            delOptRange = range(0, int(data_legnth))
            if (int(deleteOption) in delOptRange):
                print("Guest successfully deleted")
                break
            else:
                print("Entred data is incorrect. Try again")
        except Exception:
                print("That not a number")
    i=0
    for entry in temp:
        if (i == int(deleteOption)):
            pass
            i=i+1
        else:
            new_data.append(entry)
            i=i+1
        with open("guests_list.json", "w") as f:
            json.dump(new_data, f, indent=4)

def choicesFunc():

    print("----------------------------------------------------------------------------")
    print("[1] - Add guest")
    print("[2] - Delete guest")
    print("[3] - View guests list")
    print("[4] - Close program")
    try:
        global choice
        choice = int(input("Enter number: "))
        modeChoiceCheck(choice)
    except Exception:
        print("Entred data is incorrect")

#Program
while True:
    choicesFunc()
    print()

    if (choice == 1):
        addGuest()
    elif (choice == 2):
        deleteGuest()
    elif (choice == 3):
        viewGuestsList()  
    elif (choice == 4):
        quit()
    else:
        print("Entred data is incorrect. try again")    
