import sqlite3

def main_menu():
    print("Food INC staff system")
    try:
        choice = int(input("1. View Current reciepts \n2. Monitor Stock"))
        match choice:
            case 1:
                print("Current reciepts")
            case 2:
                print("Current stock")
            case _:
                print("Invalid choice")
                main_menu()
    except Exception as e:
        print("error:", e)
        main_menu()