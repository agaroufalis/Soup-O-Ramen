class Order:

    def __init__(self, place):

        # Private attributes
        self.__place = place
        self.__drinks = None
        self.__apps = None
        self.__ramen = None

    # =========================
    # GETTERS
    # =========================

    def get_place(self):
        return self.__place

    def get_drinks(self):
        return self.__drinks

    def get_apps(self):
        return self.__apps

    def get_ramen(self):
        return self.__ramen

    # =========================
    # SETTERS
    # =========================

    def set_place(self, place):
        self.__place = place

    def set_drinks(self, drinks):
        self.__drinks = drinks

    def set_apps(self, apps):
        self.__apps = apps

    def set_ramen(self, ramen):
        self.__ramen = ramen

    # =========================
    # STRING METHOD
    # =========================

    def __str__(self):

        return (
            f"Place: {self.__place}\n"
            f"Drink: {self.__drinks}\n"
            f"App: {self.__apps}\n"
            f"Ramen: {self.__ramen}"
        )
    
    # =========================
    # DISPLAY ORDER
    # =========================

    def display_order(self):

        print("\n===== CURRENT ORDER =====")

        print(f"1. Drink: {self.__drinks}")
        print(f"2. App: {self.__apps}")
        print(f"3. Size: {self.__size}")
        print(f"4. Base: {self.__base}")
        print(f"5. Spice: {self.__spice}")
        print(f"6. Add-on: {self.__addon}")     