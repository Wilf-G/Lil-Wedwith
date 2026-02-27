import time, os
import sqlite3 #Otherwise we will use SQLite



orderNumber = 0
itemsOrdered = []
LoginDetails= {
    "Username": "Password"
}

def ItemStock():
    print("What item would you like to view?")
    item = input("> ")
    #Need a check here probably using sqlite in order to check if the item they are looking for is in the database
    #if item in (database):
        #print() (Use sqlite in order to get the stock of items printed)
    #else:
        #print("That item is unavailable, try looking for something else")
        #ItemStock()

#Outputs the order in a receipt format with the items in the order
def OutputReceipt():
    print("################################")
    print(f"=========0{orderNumber}=========")
    print("################################")
    print("")
    for i in range(0, itemsOrdered):
        print(itemsOrdered[i])
    
    itemsOrdered.clear()
    time.sleep(2)
    Menu()

# Allows the user to view the stock in a database, alowing them to view one item's stock or all stock
def ManageStock():
    print("What would you like to do?")
    print("1. view stock of an item")
    print("2. View all stock")
    time.sleep(1)
    choice = int(input(""))
    if choice ==  1:
        # Different function for viewing an item's stock. Not made the function yet
        print("ItemStock")
    elif choice == 2:
        # Different function for viewing an item's stock. Not made the function yet
        print("AllStock")
    else:
        print("Invalid input, please try again")
        ManageStock()

# Allows the user to add a new  order, inputting which item they would like to add and how many items they will be adding, also gives the order a number
def NewOrder():
    global orderNumber
    print("Would you like to add new items to the order? (y/n)")
    choice = input("> ")
    while choice == "y":
        print("Enter the item to add to the order")
        item = input("> ")
        itemsOrdered.append(item)
        choice = input("Would you like to add new items to the order? (y/n)")
    print("Order added")
    Menu()

#Maybe make orders into a text file so you can search for specific orders would have to change when adding new order
def SearchOrder():
    print("Enter order to search for")
    order = input("> ") #If orders are saved as a text file the user can enter the order with file extension
    files = os.listdir(".")
    txt_files = [ f for f in files if f.endswith(".order")]

    if txt_files:
        print("Save files found:")
        for f in txt_files:
            print(f)
    else:
        print("No save files found in this folder.")
        Menu()

    saveName = input("Enter the name of your save file (without .order): ")
    saveName += ".order"

    if not os.path.exists(saveName):
        print("Save file not found!")
        return Menu()
    
    with open(saveName, "r") as file:
        lines = file.readlines()
        print(lines)

        petName = lines[0].split(":")[1].strip()

    print(f"{petName} loaded!")
    Menu()

#Menu function allowing users to select what they would like to do
def Menu():
    print("Menu")
    print("1. Output receipt")
    print("2. Check/Manage stock")
    print("3. New order")
    print("4. Search for an order")
    print("5. exit")
    choice = int(input("Enter an action: "))
    match choice:
        case 1:
            OutputReceipt()
        case 2:
            ManageStock()
        case 3:
            NewOrder()
        case 4:
            SearchOrder()
        case 5:
            itemsOrdered.clear()
            exit()
        case _:
            print("Invalid input, please try again")
            time.sleep(1)

#Function for a log in system. Need to add new users and passwords into the dictionary at the top of the program
def Login():
    print("Enter username:")
    username = input("> ")
    print("Enter password")
    password = input("> ")

    #if username is not found in dict loginDetails
    if(username not in LoginDetails):
        print("User not found!")
    #elif password is equal to the password found at username
    elif(password == LoginDetails[username]):
        print("Log in successful!")
        time.sleep(1)
        Menu()
    #if password is incorrect
    else:
        print("Password Incorrect!")
        Login()
        
Login()







