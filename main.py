from constants import MENU_FILE

from order_functions import (
    get_customer_info,
    take_order,
    edit_order,
    calculate_total
)

from file_functions import save_data_and_label


def main():

    orders = {}

    order_number = get_customer_info(orders)

    current_order = take_order(
        order_number,
        orders
    )

    current_order = edit_order(
        order_number,
        orders
    )

    total, tax = calculate_total(
        current_order,
        MENU_FILE
    )

    save_data_and_label(
        current_order,
        order_number,
        total,
        tax
    )


if __name__ == "__main__":
    main()