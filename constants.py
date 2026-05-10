import os

BASE_DIR = os.path.dirname(__file__)

DATA_FOLDER = os.path.join(BASE_DIR, "data")

MENU_FILE = os.path.join(DATA_FOLDER, "menu.txt")

DATA_FILE = os.path.join(DATA_FOLDER, "order_log.txt")

HUMAN_REPORT = os.path.join(DATA_FOLDER, "receipt.txt")

TAX_RATE = 0.05

DRINK_OPTIONS = ("Ramune", "Sake", "Sapporo", "None")

APP_OPTIONS = (
    "Karrage",
    "Edamame",
    "Tempura",
    "Takoyaki",
    "None"
)

SIZE_OPTIONS = ("Small", "Large")

BASE_OPTIONS = (
    "White",
    "Red",
    "Shoyu"
)

SPICE_OPTIONS = (
    "Mild",
    "Medium",
    "Hot"
)

ADDON_OPTIONS = (
    "Bean Sprouts",
    "Naruto",
    "Egg",
    "Corn",
    "None")