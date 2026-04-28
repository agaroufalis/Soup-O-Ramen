import streamlit as st
import datetime
import os

# Constants
MENU_FILE = "/Users/alexisgaroufalis/Library/Mobile Documents/com~apple~CloudDocs/add100/SoupFinal/Soup-O-Ramen/menu.txt"
DATA_FILE = "/Users/alexisgaroufalis/Library/Mobile Documents/com~apple~CloudDocs/add100/SoupFinal/Soup-O-Ramen/order_log.txt"
HUMAN_REPORT = "/Users/alexisgaroufalis/Library/Mobile Documents/com~apple~CloudDocs/add100/SoupFinal/Soup-O-Ramen/receipt.txt"
TAX_RATE = 0.05

DRINK_OPTIONS = ("None", "Ramune", "Sake", "Sapporo")
APP_OPTIONS = ("None", "Karrage", "Edamame", "Tempura", "Takoyaki")
SIZE_OPTIONS = ("Small", "Large")
BASE_OPTIONS = ("White", "Red", "Shoyu")
SPICE_OPTIONS = ("Mild", "Medium", "Hot")
ADDON_OPTIONS = ("None", "Bean Sprouts", "Naruto", "Egg", "Corn")

class Order:
    def __init__(self, place):
        self.place = place
        self.drinks = "None"
        self.apps = "None"
        self.ramen = ("Small", "White", "Mild", "None")

def calculate_total(order, menu_file):
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
            addon_price = menu_prices.get(addon, 0) if addon != "None" else 0
        total += ramen_price + addon_price
        tax = total * TAX_RATE
        final_total = total + tax
        return final_total, tax
    except Exception as e:
        st.error(f"Error calculating total: {str(e)}")
        return 0, 0

def save_order(order, order_number, total, tax):
    today = datetime.date.today()
    ramen_display = " ".join(order.ramen) if order.ramen else ""
    with open(DATA_FILE, "a") as f:
        f.write(f"{order_number},{order.place},{order.drinks},{order.apps},{ramen_display},{total:.2f}\n")
    receipt = f"SOUP-O-RAMEN RECEIPT - {today}\nORDER #: {order_number}\nLOCATION: {order.place}\n\nITEMS:\n Drink: {order.drinks}\n App: {order.apps}\n Ramen: {ramen_display}\n\nTAX: ${tax:.2f}\nTOTAL: ${total:.2f}\n"
    with open(HUMAN_REPORT, "w") as f:
        f.write(receipt)
    return receipt

def get_next_order_number():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                lines = f.readlines()
            if lines:
                order_nums = [int(line.split(",")[0]) for line in lines]
                return max(order_nums) + 1
        except:
            pass
    return 100

# Streamlit App
st.set_page_config(page_title="Soup-O-Ramen POS", page_icon="🍜", layout="wide")

st.title("🍜 Soup-O-Ramen POS System")

if 'orders' not in st.session_state:
    st.session_state.orders = []  # List of (order_number, order, total, tax)
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
        for i, (num, ord, tot, tax) in enumerate(st.session_state.orders):
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                st.write(f"Order {num}: {ord.place} - Total: ${tot:.2f}")
            with col2:
                if st.button(f"Edit {num}", key=f"edit_{i}"):
                    st.session_state.editing = i
            with col3:
                if st.button(f"Submit {num}", key=f"submit_{i}"):
                    receipt = save_order(ord, num, tot, tax)
                    st.success(f"Order {num} submitted!")
                    st.text(receipt)
                    st.session_state.orders.pop(i)
                    break

    # Add new order
    if st.button("Add New Order"):
        st.session_state.editing = len(st.session_state.orders)
        new_order = Order("")
        num = st.session_state.next_order_number
        st.session_state.next_order_number += 1
        total, tax = calculate_total(new_order, MENU_FILE)
        st.session_state.orders.append((num, new_order, total, tax))

    # Edit order
    if st.session_state.editing is not None:
        idx = st.session_state.editing
        num, order, _, _ = st.session_state.orders[idx]

        st.subheader(f"Editing Order {num}")

        # Customer info
        place_type = st.radio("Order Type", ["Dine-in", "To-go"], index=0 if "t" in order.place else 1, key=f"place_{idx}")
        if place_type == "Dine-in":
            table = st.number_input("Table Number", min_value=1, value=int(order.place.split('s')[0][1:]) if 't' in order.place else 1, key=f"table_{idx}")
            seat = st.number_input("Seat Number", min_value=1, value=int(order.place.split('s')[1]) if 's' in order.place else 1, key=f"seat_{idx}")
            order.place = f"t{table}s{seat}"
        else:
            name = st.text_input("Customer Name", value=order.place if order.place and 't' not in order.place else "", key=f"name_{idx}")
            order.place = name

        # Order details
        col1, col2 = st.columns(2)
        with col1:
            order.drinks = st.selectbox("Drink", DRINK_OPTIONS, index=DRINK_OPTIONS.index(order.drinks), key=f"drink_{idx}")
            order.apps = st.selectbox("Appetizer", APP_OPTIONS, index=APP_OPTIONS.index(order.apps), key=f"app_{idx}")
        with col2:
            size = st.selectbox("Size", SIZE_OPTIONS, index=SIZE_OPTIONS.index(order.ramen[0]), key=f"size_{idx}")
            base = st.selectbox("Base", BASE_OPTIONS, index=BASE_OPTIONS.index(order.ramen[1]), key=f"base_{idx}")
            spice = st.selectbox("Spice", SPICE_OPTIONS, index=SPICE_OPTIONS.index(order.ramen[2]), key=f"spice_{idx}")
            addon = st.selectbox("Add-on", ADDON_OPTIONS, index=ADDON_OPTIONS.index(order.ramen[3]), key=f"addon_{idx}")
            order.ramen = (size, base, spice, addon)

        # Calculate total
        total, tax = calculate_total(order, MENU_FILE)
        st.session_state.orders[idx] = (num, order, total, tax)
        st.write(f"**Subtotal:** ${total - tax:.2f}, **Tax:** ${tax:.2f}, **Total:** ${total:.2f}")

        if st.button("Save Changes", key=f"save_{idx}"):
            st.session_state.editing = None
            st.success("Order updated!")

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
