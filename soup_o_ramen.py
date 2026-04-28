"""
ASSIGNMENT 10B: SPRINT 3 - FUNCTIONAL STUBS
Project: Soup-O-Ramen POS (V1.0)
Developer: Alexis Garoufalis
"""

import datetime

MENU_FILE = "menu.txt"
DATA_FILE = "order_log.txt"
HUMAN_REPORT = "receipt.txt"
TAX_RATE = 0.05

# Menu validation options
DRINK_OPTIONS = ("Ramune", "Sake", "Sapporo", "None")
APP_OPTIONS = ("Karrage", "Edamame", "Tempura", "Takoyaki")
SIZE_OPTIONS = ("Small", "Large")
BASE_OPTIONS = ("White", "Red", "Shoyu")
SPICE_OPTIONS = ("Mild", "Medium", "Hot")
ADDON_OPTIONS = ("Bean Sprouts", "Naruto", "Egg", "Corn")


def get_valid_input(prompt, valid_options):
    while True:
        choice = input(prompt).title().strip()
        if choice in valid_options:
            return choice
        print(f"Invalid choice. Options: {', '.join(valid_options)}")

     
class Orders:
    def __init__(order, place, drinks=None, apps=None, ramen=None):
        order.place = place
        order.drinks = drinks
        order.apps = apps
        order.ramen = ramen

    def __str__(order):
        return (f"Place: {order.place} \nDrinks: {order.drinks} \nApps: {order.apps} \nRamen: {order.ramen}")


def process_expenses(item_name, price, quantity):

    subtotal = price * quantity
    tax = subtotal * TAX_RATE
    final_total = subtotal + tax

    summary = (
        f"\n--- Expense Summary ---\n"
        f"Item: {item_name}\n"
        f"Price: ${price:.2f}\n"
        f"Quantity: {quantity}\n"
        f"Subtotal: ${subtotal:.2f}\n"
        f"Tax (5%): ${tax:.2f}\n"
        f"Total: ${final_total:.2f}\n"
    )

    return final_total, summary

# Select the order type to determine the operation to be preformed
def get_order_type():
    
    order_type = input("Order Type (New/Edit/Cancel): ").title()
    while order_type not in ORDER_TYPE:
        print("Please choose a valid option.")
        order_type = input("Order Type (New/Edit/Cancel): ").title()
    return order_type


def get_customer_info(orders):
    order_number = 100
    if order_number in orders:
        last_order = list(orders)[-1]
        order_number = last_order + 1
    else:
        order_number = 100

    place = input("Is this order for (1)here or (2)to-go? ")

    if place == "1":
        table = input("Please enter table number: ")
        seat = input("Please enter seat number: ")
        setting = (f"t{table}s{seat} ")
        # TODO: add error checking
        orders[order_number]=Orders(setting)
        return order_number
    
    if place =="2":
        name = input("Please enter customer name: ")
        orders[order_number]=Orders(name)
        return order_number

def take_order(order_number, orders):
    cat = input("Order Category (Drinks/Apps/Ramen): ")

    orders[order_number].drinks= input("Drinks (Ramune/Sake/Sapporo/None): ").title

    orders[order_number].apps = input("Appetizers (Karrage/Edamame/Tempura/Takoyaki): ").title

    size = input("1. Size (Small/Large): ").title
    base = input("2. Base (White/Red/Shoyu): ").title
    spice = input("3. Spice (Mild/Medium/Hot): ").title
    add_ons = input("4. Add-ons (Bean Sprouts/Naruto/Soft-Boiled Egg/Sweet Corn): ").title
    orders[order_number].ramen = (size, base, spice, add_ons)
     # TODO: add error checking

def edit_order(order_number, orders):
    
    print(f"Editing order: {order_number}")
    print(f"Current order: \n{orders[order_number]}")      
    """call take_orders"""
    # TODO append edits to existing order
    

def calculate_total(order, MENU_FILE):
    total = 0
    ramen_price = 0
    addon_price = 0

    try:
        with open(MENU_FILE, "r") as f:
            for line in f:
                name, price = line.strip().split(",")
                price = float(price)

                # Drinks
                if name == order.drinks:
                    total += price

                # Apps
                if name == order.apps:
                    total += price

                # Ramen base (size-based)
                if order.ramen:
                    size = order.ramen[0]
                    if name == f"Ramen_{size}":
                        ramen_price = price

                    # Add-on pricing
                    addon = order.ramen[3]
                    if name == addon:
                        addon_price = price

    except FileNotFoundError:
        print("Menu file not found.")

    total += ramen_price + addon_price

    tax = total * TAX_RATE
    final_total = total + tax

    return final_total, tax


def save_data_and_label(order, order_number,total, tax):
    """Appends to order_history.txt and prints the human-readable label."""
   
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   

    with open(HUMAN_REPORT, "w") as file:
        file.write(f"SOUP-O-RAMEN RECEIPT - {current_time}\n")
        file.write(f"ORDER #: {order_number}\n")
        file.write(f"LOCATION: {order.place}\n\n")

        file.write("ITEMS:\n")
        file.write(f" Drink: {order.drinks}\n")
        file.write(f" App: {order.apps}\n")
        file.write(f" Ramen: {order.ramen}\n\n")

        file.write(f"TAX: ${tax:.2f}\n")
        file.write(f"TOTAL: ${total:.2f}\n")

    print("\nReceipt saved successfully!")


    with open("store_receipts.txt", "a") as file:
        file.write(f"\n[{current_time}] ORDER: {order_number}\n")
        
        for item, in order.items():
            file.write(f" - {item}:\n")
            
        file.write("----------------------\n")
    
    print("Receipt successfully logged to system!")


def main():
    orders = {}
    # 1. Identity Phase
    order_number = get_customer_info(orders = orders)
    
    # 2. Data Collection Phase
    current_order = take_order(order_number = order_number, orders = orders)

    # 3. Possible Data Editing Phase
    current_order = edit_order(order_number = order_number, orders = orders)

    # 4. Calculation Phase
    total, tax = calculate_total(current_order, MENU_FILE)

    # 5. Handoff Phase
    save_data_and_label(current_order, order_number, total, tax)

main()


