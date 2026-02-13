import time
import pandas as pd # If we need to use pandas to check database 
import sqlite3 #Otherwise we will use SQLite

#Menu system for python application
stock = pd.read_csv("", "w") #Call database using pandas but no database yet (Maybe given)

orderNumber = 0
itemsOrdered = []
LoginDetails= {
    "Username": "Password"
}

def ItemStock():
    print("What item would you like to view?")
    item = input("> ")
    #Need a check here probably using sqlite or pandas in order to check if the item they are looking for is in the database
    #if item in (database):
        #print() (Use sqlite in order to get the stock of items printed)
    #else:
        #print("That item is unavailable, try looking for something else")
        #ItemStock()

def OutputReceipt():
    print("################################")
    print(f"========={orderNumber}=========")
    print("################################")
    print("")
    for i in itemsOrdered:
        print(i)
    
    itemsOrdered.clear()
    time.sleep(2)
    Menu()

def ManageStock():
    print("What would you like to do?")
    print("1. view stock of an item")
    print("2. View all stock")
    time.sleep(1)
    choice = int(input(""))
    if choice ==  1:
        print("ItemStock")
    elif choice == 2:
        print("AllStock")
    else:
        print("Invalid input, please try again")
        ManageStock()

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
    
    #Input for what order they are searching for here

    #Output order here

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
            print("Invalid input, please try again")#
            time.sleep(1)
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





