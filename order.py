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