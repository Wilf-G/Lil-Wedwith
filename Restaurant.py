import time
import pandas as pd

#Menu system for python application

stock = pd.read_csv("", "w")

orderNumber = 0
itemsOrdered = []

def OutputReceipt():
    print("================================")
    print("orderNumber")
    print("================================")
    print("")
    print("itemsOrdered")
    itemsOrdered.clear()

def ManageStock():
    print("What would you like to do?")
    print("1. view stock of an item")
    print("2. View all stock")
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
    #Input for what to add here

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
            Menu()
