import streamlit as st
import datetime
import os
from blueprints import Order
import requests

# Constants
MENU_FILE = (
    "https://raw.githubusercontent.com/agaroufalis/Soup-O-Ramen/"
    "main/data/menu.txt"
)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT_DIR, "order_log.txt")
HUMAN_REPORT = os.path.join(ROOT_DIR, "receipt.txt")
TAX_RATE = 0.05

DRINK_OPTIONS = ("None", "Ramune", "Sake", "Sapporo")
APP_OPTIONS = ("None", "Karrage", "Edamame", "Tempura", "Takoyaki")
SIZE_OPTIONS = ("Small", "Large")
BASE_OPTIONS = ("White", "Red", "Shoyu")
SPICE_OPTIONS = ("Mild", "Medium", "Hot")
ADDON_OPTIONS = ("None", "Bean Sprouts", "Naruto", "Egg", "Corn")


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


@st.cache_data(ttl=300)
def load_menu(menu_file):
    """Load menu prices from a URL or local file."""
    menu_prices = {}

    if menu_file.startswith("http"):
        response = requests.get(menu_file, timeout=10)
        response.raise_for_status()
        lines = response.text.strip().splitlines()
    else:
        with open(menu_file, "r") as f:
            lines = f.readlines()

    for line in lines:
        if not line.strip():
            continue
        name, price = line.strip().split(",")
        menu_prices[name] = float(price)

    return menu_prices


def calculate_total(order, menu_file):
    """Calculate the total cost and tax for an order."""
    try:
        menu_prices = load_menu(menu_file)
        total = 0

        if order.drinks and order.drinks != "None":
            total += menu_prices.get(order.drinks, 0)
        if order.apps and order.apps != "None":
            total += menu_prices.get(order.apps, 0)
        if order.ramen:
            size = order.ramen[0]
            total += menu_prices.get(f"Ramen_{size}", 0)
            addon = order.ramen[3]
            if addon != "None":
                total += menu_prices.get(addon, 0)

        tax = total * TAX_RATE
        return total + tax, tax
    except Exception as e:
        st.error(f"Error calculating total: {str(e)}")
        return 0, 0


def format_ramen(order):
    return " ".join(order.ramen) if order.ramen else ""


def create_order_entry(num):
    new_order = Order("")
    total, tax = calculate_total(new_order, MENU_FILE)
    return {
        'num': num,
        'order': new_order,
        'total': total,
        'tax': tax,
        'is_saved': False,
        'is_submitted': False
    }


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


def add_new_order():
    num = st.session_state.next_order_number
    st.session_state.next_order_number += 1
    st.session_state.orders.append(create_order_entry(num))
    st.success(f"✅ Order {num} created! Edit details below and click 'Save Changes' when ready.")


def render_edit_form(idx):
    """Render the edit form for an order."""
    order_dict = st.session_state.orders[idx]
    num = order_dict['num']
    order_obj = order_dict['order']
    is_saved = order_dict['is_saved']

    st.subheader(f"Editing Order {num}")
    if is_saved:
        st.info("⚠️ This order has been saved. Customer info is now locked. You can still edit items and re-save if needed.")

    # Customer info
    place_type = st.radio(
        "Order Type",
        ["Dine-in", "To-go"],
        index=(
            0 if "t" in order_obj.place
            else 1 if order_obj.place else 0
        ),
        key=f"place_type_{idx}",
        disabled=is_saved,
        help="Select 'Dine-in' for table seating or 'To-go' for takeout orders"
    )
    if place_type == "Dine-in":
        table = st.number_input(
            "Table Number",
            min_value=1,
            value=(
                int(order_obj.place.split('s')[0][1:])
                if 't' in order_obj.place else 1
            ),
            key=f"table_{idx}",
            help="Which table is the customer at?"
        )
        seat = st.number_input(
            "Seat Number",
            min_value=1,
            value=(
                int(order_obj.place.split('s')[1])
                if 's' in order_obj.place else 1
            ),
            key=f"seat_{idx}",
            help="Which seat at the table?"
        )
        order_obj.place = f"t{table}s{seat}"
    else:
        name = st.text_input(
            "Customer Name",
            value=(
                order_obj.place if order_obj.place
                and 't' not in order_obj.place else ""
            ),
            key=f"name_{idx}",
            placeholder="Enter customer name for takeout",
            help="Name to call when order is ready"
        )
        order_obj.place = name

    # Order details
    col1, col2 = st.columns(2)
    with col1:
        order_obj.drinks = st.selectbox(
            "Drink",
            DRINK_OPTIONS,
            index=DRINK_OPTIONS.index(order_obj.drinks),
            key=f"drink_{idx}",
            help="Select a beverage or 'None' for no drink"
        )
        order_obj.apps = st.selectbox(
            "Appetizer",
            APP_OPTIONS,
            index=APP_OPTIONS.index(order_obj.apps),
            key=f"app_{idx}",
            help="Select a side dish or 'None' to skip"
        )
    with col2:
        st.markdown("**Ramen Customization:**")
        size = st.selectbox(
            "Size",
            SIZE_OPTIONS,
            index=SIZE_OPTIONS.index(order_obj.ramen[0]),
            key=f"size_{idx}",
            help="Choose portion size"
        )
        base = st.selectbox(
            "Broth Base",
            BASE_OPTIONS,
            index=BASE_OPTIONS.index(order_obj.ramen[1]),
            key=f"base_{idx}",
            help="White: mild pork, Red: spicy miso, Shoyu: soy-based"
        )
        spice = st.selectbox(
            "Spice Level",
            SPICE_OPTIONS,
            index=SPICE_OPTIONS.index(order_obj.ramen[2]),
            key=f"spice_{idx}",
            help="How spicy should it be?"
        )
        addon = st.selectbox(
            "Add-on",
            ADDON_OPTIONS,
            index=ADDON_OPTIONS.index(order_obj.ramen[3]),
            key=f"addon_{idx}",
            help="Optional toppings for extra flavor"
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

    button_col1, button_col2 = st.columns([1, 1])
    with button_col1:
        if st.button("Save Changes", key=f"save_{idx}"):
            st.session_state.orders[idx]['is_saved'] = True
            st.session_state.editing = None
            st.success("Order updated!")
            st.rerun()
    with button_col2:
        if st.button("Cancel", key=f"cancel_{idx}"):
            st.session_state.editing = None
            st.info("Edit cancelled. Order remains unchanged.")
            st.rerun()


def render_order_row(order_dict, index):
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
        if not is_submitted:
            if st.button(f"Edit {num}", key=f"edit_{index}"):
                st.session_state.editing = index
    with col3:
        if is_saved and not is_submitted:
            if st.button(f"Submit {num}", key=f"submit_{index}"):
                receipt = save_order(order_obj, num, tot, tax)
                st.success(f"✅ Order {num} submitted!")
                st.divider()
                st.text(receipt)
                st.divider()
                st.session_state.orders[index]['is_submitted'] = True
        elif not is_saved and not is_submitted:
            if st.button(f"Delete {num}", key=f"delete_{index}", type="secondary"):
                st.session_state.delete_confirm = index
        
        if st.session_state.get('delete_confirm') == index:
            st.warning(f"⚠️ Are you sure you want to delete Order {num}?")
            dcol1, dcol2 = st.columns([1, 1])
            with dcol1:
                if st.button(f"Yes, delete Order {num}", key=f"confirm_delete_{index}", type="primary"):
                    st.session_state.orders.pop(index)
                    st.session_state.delete_confirm = None
                    st.success(f"Order {num} deleted!")
                    st.rerun()
            with dcol2:
                if st.button(f"Cancel", key=f"cancel_delete_{index}"):
                    st.session_state.delete_confirm = None
                    st.rerun()


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
if 'delete_confirm' not in st.session_state:
    st.session_state.delete_confirm = None  # Index of order pending deletion confirmation

menu = ["Manage Orders", "View Past Orders"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Manage Orders":
    st.header("Order Management")
    st.markdown(
        "Use `Add New Order` to start a customer order, `Edit` to adjust details, "
        "and `Submit` to write it to the order log. Saved orders can be submitted, "
        "while unsaved orders can be edited or deleted."
    )
    st.write("---")

    # Display current orders
    if st.session_state.orders:
        st.subheader("Current Session Orders")
        st.caption(
            f"You currently have {len(st.session_state.orders)} order(s) in this session."
        )
        for i, order_dict in enumerate(st.session_state.orders):
            render_order_row(order_dict, i)

    # Add new order
    if st.button("Add New Order"):
        st.session_state.editing = len(st.session_state.orders)
        add_new_order()

    if st.session_state.editing is not None:
        idx = st.session_state.editing
        if idx < len(st.session_state.orders):
            render_edit_form(idx)
        else:
            st.session_state.editing = None

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
