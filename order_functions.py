from order import Order

from validation import (
    get_valid_input,
    get_non_empty_input,
    get_positive_int
)

from constants import *


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


def take_order(order_number, orders):

    order = orders[order_number]

    order.set_drinks(
        get_valid_input(
            "Drink: ",
            DRINK_OPTIONS
        )
    )

    order.set_apps(
        get_valid_input(
            "App: ",
            APP_OPTIONS
        )
    )

    size = get_valid_input(
        "Size: ",
        SIZE_OPTIONS
    )

    base = get_valid_input(
        "Base: ",
        BASE_OPTIONS
    )

    spice = get_valid_input(
        "Spice: ",
        SPICE_OPTIONS
    )

    addon = get_valid_input(
        "Add-on: ",
        ADDON_OPTIONS
    )

    order.set_ramen(
        (
            size,
            base,
            spice,
            addon
        )
    )

    return order


def edit_order(order_number, orders):

    print("\nCurrent Order:")
    print(orders[order_number])

    choice = get_valid_input(
        "Edit order? (Y/N): ",
        ("Y", "N")
    )

    if choice == "Y":
        return take_order(order_number, orders)

    return orders[order_number]


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
                if name == order.get_drinks():
                    total += price

                # Apps
                if name == order.get_apps():
                    total += price

                # Ramen
                if order.get_ramen():

                    size = order.get_ramen()[0]

                    if name == f"Ramen_{size}":
                        ramen_price = price

                    addon = order.get_ramen()[3]

                    if name == addon:
                        addon_price = price

    except FileNotFoundError:

        print("Menu file not found.")

    total += ramen_price + addon_price

    tax = total * TAX_RATE

    final_total = total + tax

    return final_total, tax