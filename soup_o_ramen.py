"""
ASSIGNMENT 10B: SPRINT 3 - FUNCTIONAL STUBS
Project: Soup-O-Ramen POS (V1.0)
Developer: Alexis Garoufalis
"""

import datetime

# =========================
# GLOBAL CONSTANTS
# =========================
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


# =========================
# VALIDATION HELPERS
# =========================
def get_valid_input(prompt, valid_options):
    while True:
        choice = input(prompt).title().strip()
        if choice in valid_options:
            return choice
        print(f"Invalid choice. Options: {', '.join(valid_options)}")


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be blank.")


def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Must be greater than 0.")
        except ValueError:
            print("Enter a valid number.")


# =========================
# ORDER CLASS
# =========================
class Order:
    def __init__(self, place):
        self.place = place
        self.drinks = None
        self.apps = None
        self.ramen = None

    def __str__(self):
        return (
            f"Place: {self.place}\n"
            f"Drink: {self.drinks}\n"
            f"App: {self.apps}\n"
            f"Ramen: {self.ramen}"
        )


# =========================
# CUSTOMER SETUP
# =========================
def get_customer_info(orders):
    if orders:
        order_number = max(orders.keys()) + 1
    else:
        order_number = 100

    place = get_valid_input(
        "Is this order for (1) here or (2) to-go? ",
        ("1", "2")
    )

    if place == "1":
        table = get_positive_int("Table number: ")
        seat = get_positive_int("Seat number: ")
        setting = f"t{table}s{seat}"
        orders[order_number] = Order(setting)
    else:
        name = get_non_empty_input("Customer name: ")
        orders[order_number] = Order(name)

    return order_number


# =========================
# ORDER INPUT
# =========================
def take_order(order_number, orders):
    order = orders[order_number]

    order.drinks = get_valid_input("Drink: ", DRINK_OPTIONS)
    order.apps = get_valid_input("App: ", APP_OPTIONS)

    size = get_valid_input("Size: ", SIZE_OPTIONS)
    base = get_valid_input("Base: ", BASE_OPTIONS)
    spice = get_valid_input("Spice: ", SPICE_OPTIONS)
    addon = get_valid_input("Add-on: ", ADDON_OPTIONS)

    order.ramen = (size, base, spice, addon)

    return order


def edit_order(order_number, orders):
    print("\nCurrent Order:")
    print(orders[order_number])

    choice = get_valid_input("Edit order? (Y/N): ", ("Y", "N"))
    if choice == "Y":
        return take_order(order_number, orders)

    return orders[order_number]


# =========================
# CALCULATION 
# =========================
def calculate_total(order, menu_file):
    total = 0
    ramen_price = 0
    addon_price = 0

    try:
        with open(menu_file, "r") as f:
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


# =========================
# FILE OUTPUT
# =========================
def save_data_and_label(order, order_number, total, tax):
    today = datetime.date.today()

    # RAW DATA (append)
    with open(DATA_FILE, "a") as f:
        f.write(
            f"{order_number},{order.place},{order.drinks},"
            f"{order.apps},{order.ramen},{total:.2f}\n"
        )

    # HUMAN RECEIPT (overwrite)
    with open(HUMAN_REPORT, "w") as f:
        f.write(f"SOUP-O-RAMEN RECEIPT - {today}\n")
        f.write(f"ORDER #: {order_number}\n")
        f.write(f"LOCATION: {order.place}\n\n")

        f.write("ITEMS:\n")
        f.write(f" Drink: {order.drinks}\n")
        f.write(f" App: {order.apps}\n")
        f.write(f" Ramen: {order.ramen}\n\n")

        f.write(f"TAX: ${tax:.2f}\n")
        f.write(f"TOTAL: ${total:.2f}\n")

    print("\nReceipt saved successfully!")


# =========================
# MAIN
# =========================
def main():
    orders = {}

    # 1. Identity Phase
    order_number = get_customer_info(orders)

    # 2. Order Input
    current_order = take_order(order_number, orders)

    # 3. Edit Phase
    current_order = edit_order(order_number, orders)

    # 4. Calculation Phase
    total, tax = calculate_total(current_order, MENU_FILE)

    # 5. Output Phase
    save_data_and_label(current_order, order_number, total, tax)


if __name__ == "__main__":
    main()