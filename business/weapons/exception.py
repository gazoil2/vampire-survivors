class InvalidItemError(Exception):
    def __init__(self, item, message="Invalid item"):
        self.item = item
        self.message = message
        super().__init__(f"{message}: {type(item).__name__}")

class FullInventoryError(Exception):
    def __init__(self, message= "The inventory is full"):
        super().__init__(message)

class InvalidLevelUp(Exception):
    def __init__(self, message= "There is no more levels for this pasive item/ weapon"):
        super().__init__(message)

class ItemNotFoundError(Exception):
    """Raised when an item is not found in the inventory."""
    def __init__(self, item):
        super().__init__(f"Item '{item}' not found in inventory.")
        self.item = item
