import datetime

from constants import DATA_FILE
from constants import HUMAN_REPORT


def save_data_and_label(
        order,
        order_number,
        total,
        tax
):

    today = datetime.date.today()

    # =========================
    # RAW DATA FILE
    # =========================

    with open(DATA_FILE, "a") as f:

        f.write(
            f"{order_number},"
            f"{order.get_place()},"
            f"{order.get_drinks()},"
            f"{order.get_apps()},"
            f"{order.get_ramen()},"
            f"{total:.2f}\n"
        )

    # =========================
    # RECEIPT FILE
    # =========================

    with open(HUMAN_REPORT, "w") as f:

        f.write(
            f"SOUP-O-RAMEN RECEIPT - {today}\n"
        )

        f.write(
            f"ORDER #: {order_number}\n"
        )

        f.write(
            f"LOCATION: {order.get_place()}\n\n"
        )

        f.write("ITEMS:\n")

        f.write(
            f" Drink: {order.get_drinks()}\n"
        )

        f.write(
            f" App: {order.get_apps()}\n"
        )

        f.write(
            f" Ramen: {order.get_ramen()}\n\n"
        )

        f.write(
            f"TAX: ${tax:.2f}\n"
        )

        f.write(
            f"TOTAL: ${total:.2f}\n"
        )

    print("\nReceipt saved successfully!")