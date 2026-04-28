import streamlit as st
import datetime
import os
from dataclasses import dataclass

# Constants
MENU_FILE = (
    "/Users/alexisgaroufalis/Library/Mobile Documents/"
    "com~apple~CloudDocs/add100/SoupFinal/Soup-O-Ramen/menu.txt"
)
DATA_FILE = (
    "/Users/alexisgaroufalis/Library/Mobile Documents/"
    "com~apple~CloudDocs/add100/SoupFinal/Soup-O-Ramen/order_log.txt"
)
HUMAN_REPORT = (
    "/Users/alexisgaroufalis/Library/Mobile Documents/"
    "com~apple~CloudDocs/add100/SoupFinal/Soup-O-Ramen/receipt.txt"
)
TAX_RATE = 0.05

DRINK_OPTIONS = ("None", "Ramune", "Sake", "Sapporo")
APP_OPTIONS = ("None", "Karrage", "Edamame", "Tempura", "Takoyaki")
SIZE_OPTIONS = ("Small", "Large")
BASE_OPTIONS = ("White", "Red", "Shoyu")
SPICE_OPTIONS = ("Mild", "Medium", "Hot")
ADDON_OPTIONS = ("None", "Bean Sprouts", "Naruto", "Egg", "Corn")


@dataclass
class Order:
    """Represents a customer order."""
    place: str
    drinks: str = "None"
    apps: str = "None"
    ramen: tuple = ("Small", "White", "Mild", "None")


def get_next_order_number():
    """Get the next order number based on existing log."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                lines = f.readlines()
            if lines:
                order_nums = [int(line.split(",")[0]) for line in lines]
                return max(order_nums) + 1
        except (ValueError, IndexError):
            pass
    return 100


def calculate_total(order, menu_file):
    """Calculate the total cost and tax for an order."""
    try:
        total = 0
        ramen_price = 0
        addon_price = 0
        menu_prices = {}
        with open(menu_file, "r") as f:
            for line in f:
                name, price = line.strip().split(",")
                menu_prices[name] = float(price)

        if order.drinks and order.drinks != "None":
            total += menu_prices.get(order.drinks, 0)
        if order.apps and order.apps != "None":
            total += menu_prices.get(order.apps, 0)
        if order.ramen:
            size = order.ramen[0]
            ramen_price = menu_prices.get(f"Ramen_{size}", 0)
            addon = order.ramen[3]
            addon_price = (
                menu_prices.get(addon, 0) if addon != "None" else 0
            )
        total += ramen_price + addon_price
        tax = total * TAX_RATE
        final_total = total + tax
        return final_total, tax
    except Exception as e:
        st.error(f"Error calculating total: {str(e)}")
        return 0, 0


def save_order(order, order_number, total, tax):
    """Save the order to files and return the receipt."""
    today = datetime.date.today()
    ramen_display = " ".join(order.ramen) if order.ramen else ""
    with open(DATA_FILE, "a") as f:
        f.write(
            f"{order_number},{order.place},{order.drinks},"
            f"{order.apps},{ramen_display},{total:.2f}\n"
        )
    receipt = (
        f"SOUP-O-RAMEN RECEIPT - {today}\n"
        f"ORDER #: {order_number}\n"
        f"LOCATION: {order.place}\n\n"
        "ITEMS:\n"
        f" Drink: {order.drinks}\n"
        f" App: {order.apps}\n"
        f" Ramen: {ramen_display}\n\n"
        f"TAX: ${tax:.2f}\n"
        f"TOTAL: ${total:.2f}\n"
    )
    with open(HUMAN_REPORT, "w") as f:
        f.write(receipt)
    return receipt


# Streamlit App
st.set_page_config(
    page_title="Soup-O-Ramen POS",
    page_icon="🍜",
    layout="wide"
)

st.title("🍜 Soup-O-Ramen POS System")

if 'orders' not in st.session_state:
    st.session_state.orders = []  # List of order dicts
if 'editing' not in st.session_state:
    st.session_state.editing = None  # Index of order being edited
if 'next_order_number' not in st.session_state:
    st.session_state.next_order_number = get_next_order_number()

menu = ["Manage Orders", "View Past Orders"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Manage Orders":
    st.header("Order Management")

    # Display current orders
    if st.session_state.orders:
        st.subheader("Current Session Orders")
        for i, order_dict in enumerate(st.session_state.orders):
            num = order_dict['num']
            order_obj = order_dict['order']
            tot = order_dict['total']
            tax = order_dict['tax']
            is_saved = order_dict['is_saved']
            is_submitted = order_dict['is_submitted']

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                status = (
                    " (Submitted)" if is_submitted
                    else " (Unsaved)" if not is_saved
                    else ""
                )
                st.write(
                    f"Order {num}: {order_obj.place} - "
                    f"Total: ${tot:.2f}{status}"
                )
            with col2:
                if is_saved and not is_submitted:
                    if st.button(f"Edit {num}", key=f"edit_{i}"):
                        st.session_state.editing = i
                elif not is_saved and not is_submitted:
                    if st.button(f"Edit {num}", key=f"edit_{i}"):
                        st.session_state.editing = i
            with col3:
                if is_saved and not is_submitted:
                    if st.button(f"Submit {num}", key=f"submit_{i}"):
                        receipt = save_order(
                            order_obj, num, tot, tax
                        )
                        st.success(f"Order {num} submitted!")
                        st.text(receipt)
                        # Update the item
                        st.session_state.orders[i]['is_submitted'] = True
                elif not is_saved and not is_submitted:
                    if st.button(f"Delete {num}", key=f"delete_{i}"):
                        st.session_state.orders.pop(i)
                        st.success(f"Order {num} deleted!")
                        st.rerun()
                        break

    # Add new order
    if st.button("Add New Order"):
        st.session_state.editing = len(st.session_state.orders)
        new_order = Order("")
        num = st.session_state.next_order_number
        st.session_state.next_order_number += 1
        total, tax = calculate_total(new_order, MENU_FILE)
        st.session_state.orders.append({
            'num': num,
            'order': new_order,
            'total': total,
            'tax': tax,
            'is_saved': False,
            'is_submitted': False
        })

    # Edit order
    if st.session_state.editing is not None:
        idx = st.session_state.editing
        order_dict = st.session_state.orders[idx]
        num = order_dict['num']
        order_obj = order_dict['order']
        is_saved = order_dict['is_saved']
        is_submitted = order_dict['is_submitted']

        st.subheader(f"Editing Order {num}")

        # Customer info
        place_type = st.radio(
            "Order Type",
            ["Dine-in", "To-go"],
            index=(
                0 if "t" in order_obj.place
                else 1 if order_obj.place else 0
            ),
            key=f"place_type_{idx}"
        )
        if place_type == "Dine-in":
            table = st.number_input(
                "Table Number",
                min_value=1,
                value=(
                    int(order_obj.place.split('s')[0][1:])
                    if 't' in order_obj.place else 1
                ),
                key=f"table_{idx}"
            )
            seat = st.number_input(
                "Seat Number",
                min_value=1,
                value=(
                    int(order_obj.place.split('s')[1])
                    if 's' in order_obj.place else 1
                ),
                key=f"seat_{idx}"
            )
            order_obj.place = f"t{table}s{seat}"
        else:
            name = st.text_input(
                "Customer Name",
                value=(
                    order_obj.place if order_obj.place
                    and 't' not in order_obj.place else ""
                ),
                key=f"name_{idx}"
            )
            order_obj.place = name

        # Order details
        col1, col2 = st.columns(2)
        with col1:
            order_obj.drinks = st.selectbox(
                "Drink",
                DRINK_OPTIONS,
                index=DRINK_OPTIONS.index(order_obj.drinks),
                key=f"drink_{idx}"
            )
            order_obj.apps = st.selectbox(
                "Appetizer",
                APP_OPTIONS,
                index=APP_OPTIONS.index(order_obj.apps),
                key=f"app_{idx}"
            )
        with col2:
            size = st.selectbox(
                "Size",
                SIZE_OPTIONS,
                index=SIZE_OPTIONS.index(order_obj.ramen[0]),
                key=f"size_{idx}"
            )
            base = st.selectbox(
                "Base",
                BASE_OPTIONS,
                index=BASE_OPTIONS.index(order_obj.ramen[1]),
                key=f"base_{idx}"
            )
            spice = st.selectbox(
                "Spice",
                SPICE_OPTIONS,
                index=SPICE_OPTIONS.index(order_obj.ramen[2]),
                key=f"spice_{idx}"
            )
            addon = st.selectbox(
                "Add-on",
                ADDON_OPTIONS,
                index=ADDON_OPTIONS.index(order_obj.ramen[3]),
                key=f"addon_{idx}"
            )
            order_obj.ramen = (size, base, spice, addon)

        # Calculate total
        total, tax = calculate_total(order_obj, MENU_FILE)
        st.session_state.orders[idx]['total'] = total
        st.session_state.orders[idx]['tax'] = tax
        st.write(
            f"**Subtotal:** ${total - tax:.2f}, "
            f"**Tax:** ${tax:.2f}, **Total:** ${total:.2f}"
        )

        if st.button("Save Changes", key=f"save_{idx}"):
            st.session_state.orders[idx]['is_saved'] = True
            st.session_state.editing = None
            st.success("Order updated!")
            st.rerun()

elif choice == "View Past Orders":
    st.header("Past Orders")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            lines = f.readlines()
        if lines:
            # Parse and display nicely
            orders = []
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    orders.append({
                        "Order #": parts[0],
                        "Place": parts[1],
                        "Drink": parts[2],
                        "App": parts[3],
                        "Ramen": parts[4],
                        "Total": f"${parts[5]}"
                    })
            st.table(orders)
        else:
            st.info("No past orders.")
    else:
        st.info("No order log found.")
